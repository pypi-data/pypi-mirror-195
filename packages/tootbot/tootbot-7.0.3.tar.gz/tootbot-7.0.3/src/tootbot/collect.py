"""Helper classes and methods to assist with the collection of content to be posted to Mastodon."""
import asyncio
import configparser
import hashlib
import logging
import os
import re
from typing import Any
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import TypeVar
from urllib.parse import urlsplit

import aiofiles
import aiohttp
import asyncpraw.exceptions
import asyncprawcore
import magic
import yt_dlp.utils
from asyncpraw.models import Submission
from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientError
from tqdm import tqdm
from tqdm.asyncio import tqdm as aiotqdm

from . import PROGRESS_BAR_FORMAT
from . import USER_AGENT
from . import __display_name__
from .control import Configuration
from .control import Secret
from .control import SubredditConfig

logger = logging.getLogger(__display_name__)

RH = TypeVar("RH", bound="RedditHelper")
LMH = TypeVar("LMH", bound="LinkedMediaHelper")
MA = TypeVar("MA", bound="MediaAttachment")


async def get_file(img_url: str, file_path: str, progress_label: str) -> Optional[str]:
    """Save a file located at img_url to a file located at filepath.

    :param img_url: url of imgur image to download
    :param file_path: directory and filename where to save the downloaded image to
    :param progress_label: Message to add to progress bar

    :returns:
        file_path (string): path to downloaded image or None if no image was downloaded
    """
    logger.debug(
        "collect.py - get_file(img_url=%s, file_path=%s, progress_label=%s)",
        img_url,
        file_path,
        progress_label,
    )
    chunk_size = 64 * 1024
    try:
        client = aiohttp.ClientSession(raise_for_status=True)
        meta = await client.head(url=img_url)
        download_size = int(meta.headers["content-length"])

        file_out = await aiofiles.open(file=file_path, mode="wb")
        progress_bar = tqdm(
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
            desc=f"{progress_label:.<60}",
            ncols=120,
            total=download_size,
            leave=True,
        )
        response = await client.get(url=img_url)
        async for data_chunk in response.content.iter_chunked(chunk_size):
            await file_out.write(data_chunk)
            progress_bar.update(len(data_chunk))

        await file_out.close()
        await client.close()
        await asyncio.sleep(0)  # allow client session to close before continuing
        logger.debug("collect.py - get_file(...) -> file_path=%s", file_path)
        return file_path

    except aiohttp.ClientError as save_image_error:
        logger.error(
            "collect.py - get_file(...) -> None - download failed with: %s",
            save_image_error,
        )
        return None


async def get_secrets(config_dir: str) -> Dict[str, Secret]:
    """Collect all api secrets either from already store secrets files or from user input.

    :param config_dir: directory to check read config.ini file from
    """
    secrets = {}
    secrets["reddit"] = await _get_reddit_secret(config_dir=config_dir)
    secrets["imgur"] = _get_imgur_secret(config_dir=config_dir)

    return secrets


async def _get_reddit_secret(config_dir: str) -> Secret:
    """Collect reddit secret from stored secrets file or from user input.

    :param config_dir: directory to check read config.ini file from
    """
    reddit_secrets_file = f"{config_dir}/reddit.secret"  # pragma: allowlist secret
    reddit_config = configparser.ConfigParser()
    if not os.path.exists(reddit_secrets_file):
        print("Reddit API keys not found. Please provide Reddit API values.")
        print("(See wiki if you need help).")
        # Whitespaces are stripped from input: https://stackoverflow.com/a/3739939
        reddit_agent = "".join(input("[ .. ] Enter Reddit agent: ").split())
        reddit_client_secret = "".join(
            input("[ .. ] Enter Reddit client secret: ").split()
        )
        # Make sure authentication is working
        # create Reddit api connection and load posts from announcements subreddit
        # to confirm reddit connection works
        reddit_client = asyncpraw.Reddit(
            user_agent="Tootbot",
            client_id=reddit_agent,
            client_secret=reddit_client_secret,
        )
        subreddit = await reddit_client.subreddit("announcements")
        async for _post in subreddit.hot():
            continue

        # It worked, so save the keys to a file
        reddit_config["Reddit"] = {
            "Agent": reddit_agent,
            "ClientSecret": reddit_client_secret,
        }
        with open(reddit_secrets_file, "w", encoding="utf8") as new_reddit_secrets:
            reddit_config.write(new_reddit_secrets)
    else:
        # Read API keys from secret file
        reddit_config.read(reddit_secrets_file)

    return Secret(
        client_id=reddit_config["Reddit"]["Agent"],
        client_secret=reddit_config["Reddit"]["ClientSecret"],
    )


def _get_imgur_secret(config_dir: str) -> Secret:
    """Check if the Imgur api secrets file exists.

    - If the file exists, this method reads the imgur secrets file and returns the
      secrets a Secret dataclass.
    - If the file doesn't exist it asks the user over stdin to supply these values
      and then saves them into the imgur_secrets file

    :param config_dir: directory to check read config.ini file from

    :returns:
        api_secrets (Secret): instance of Secret class containing the api secrets
        to work with imgur
    """
    secrets_file = f"{config_dir}/imgur.secret"  # pragma: allowlist secret
    if not os.path.exists(secrets_file):
        print("Imgur API keys not found. (See wiki if you need help).")

        # Whitespaces are stripped from input: https://stackoverflow.com/a/3739939
        imgur_client_id = "".join(input("[ .. ] Enter Imgur client ID: ").split())
        imgur_client_secret = "".join(
            input("[ .. ] Enter Imgur client secret: ").split()
        )
        # Make sure authentication is working
        imgur_client = ImgurClient(imgur_client_id, imgur_client_secret)

        # If this call doesn't work, it'll throw an ImgurClientError
        imgur_client.get_album("dqOyj")
        # It worked, so save the keys to a file
        imgur_config = configparser.ConfigParser()
        imgur_config["Imgur"] = {
            "ClientID": imgur_client_id,
            "ClientSecret": imgur_client_secret,
        }
        with open(secrets_file, "w", encoding="UTF-8") as file:
            imgur_config.write(file)
    else:
        # Read API keys from secret file
        imgur_config = configparser.ConfigParser()
        imgur_config.read(secrets_file)

    return Secret(
        client_id=imgur_config["Imgur"]["ClientID"],
        client_secret=imgur_config["Imgur"]["ClientSecret"],
    )


class RedditHelper:
    """RedditHelper provides methods to collect data / content from reddit to
    then post on Mastodon.
    """

    # Check if reddit access details in 'reddit.secret' file has already been set up
    # and load it, otherwise guide user through setting it up.
    def __init__(self: RH, config: Configuration, api_secret: Secret) -> None:
        """Initialise RedditHelper instance.

        :param config: Configuration settings
        :param api_secret: Secrets to use with reddit api
        """
        self.config = config
        self.posts: Dict[str, asyncpraw.models.Submission] = {}
        self.api_secret = api_secret

    async def get_all_reddit_posts(self: RH) -> None:
        """Collect posts from all configured subreddits."""
        tasks = []

        reddit_con = asyncpraw.Reddit(
            user_agent=USER_AGENT,
            client_id=self.api_secret.client_id,
            client_secret=self.api_secret.client_secret,
        )

        for subreddit in self.config.subreddits:
            tasks.append(self.get_reddit_posts(subreddit, reddit_con))
        progress_title = "Processing Subreddits"
        task_results = await aiotqdm.gather(
            *tasks,
            desc=f"{progress_title:.<60}",
            ncols=120,
            bar_format=PROGRESS_BAR_FORMAT,
            total=len(tasks),
        )

        for result in task_results:
            self.posts.update(result)

        await reddit_con.close()

    async def get_reddit_posts(
        self: RH,
        subreddit: SubredditConfig,
        reddit_con: asyncpraw.Reddit,
    ) -> Dict[str, asyncpraw.models.Submission]:
        """Collect posts considered hot from configured sub/multi-reddits.

        :param subreddit: subreddits to check for posts to x-post
        :param reddit_con: API reference

        :returns:
        Dictionary with str of tags to use and subreddit posts
        """
        posts = {}
        logger.debug("Retrieving posts from %s", subreddit.name)
        try:
            subreddit_info = await reddit_con.subreddit(subreddit.name)
            subreddit_posts: Dict[str, asyncpraw.models.Submission] = {}
            async for submission in subreddit_info.hot(
                limit=self.config.reddit.post_limit
            ):
                subreddit_posts[submission.id] = submission
            posts[subreddit.tags] = subreddit_posts
        except asyncprawcore.AsyncPrawcoreException as reddit_error:
            logger.warning(
                "Error when getting reddit posts from r/%s: %s",
                subreddit.name,
                reddit_error,
            )
        return posts

    async def winnow_reddit_posts(self: RH) -> None:
        """Filter out reddit posts according to configuration and whether it has already been posted."""
        recorder = self.config.bot.post_recorder
        nsfw_allowed = self.config.reddit.nsfw_allowed
        self_posts_allowed = self.config.reddit.self_posts
        spoilers_allowed = self.config.reddit.spoilers
        stickied_allowed = self.config.reddit.stickied_allowed

        title = "Winnowing chaff "
        for posts in tqdm(
            self.posts.values(),
            desc=f"{title:.<60}",
            total=len(self.posts),
            ncols=120,
            bar_format=PROGRESS_BAR_FORMAT,
        ):
            post_ids = list(posts.keys())
            for post_id in post_ids:
                if posts[post_id].over_18 and not nsfw_allowed:
                    # Skip over NSFW posts if they are disabled in the config file
                    logger.debug("Skipping %s, it is marked as NSFW", post_id)
                    del posts[post_id]
                    continue

                if posts[post_id].is_self and not self_posts_allowed:
                    # Skip over NSFW posts if they are disabled in the config file
                    logger.debug("Skipping %s, it is a self post", post_id)
                    del posts[post_id]
                    continue

                if posts[post_id].spoiler and not spoilers_allowed:
                    # Skip over posts marked as spoilers if they are disabled in
                    # the config file
                    logger.debug("Skipping %s, it is marked as a spoiler", post_id)
                    del posts[post_id]
                    continue

                if posts[post_id].stickied and not stickied_allowed:
                    logger.debug("Skipping %s, it is stickied", post_id)
                    del posts[post_id]
                    continue

                if await recorder.duplicate_check(post_id):
                    logger.debug("Skipping %s, it has already been tooted", post_id)
                    del posts[post_id]
                    continue

                if await recorder.duplicate_check(posts[post_id].url):
                    logger.debug("Skipping %s, it has already been tooted", post_id)
                    del posts[post_id]
                    continue

    def get_caption(
        self: RH,
        submission: Submission,
        max_len: int,
        add_hash_tags: Optional[str] = None,
        promo_message: Optional[str] = None,
    ) -> str:
        """get_caption returns the text to be posted to mastodon. This is
        determined from the text of the reddit submission, if a promo message
        should be included, and any hashtags.

        :param submission: PRAW Submission object for the reddit post we are
            determining the mastodon toot text for.
        :param max_len: The maximum length the text for the mastodon toot can be.
        :param add_hash_tags: additional hashtags to be added to global hashtags
            defined in config file. The hashtags must be comma delimited
        :param promo_message: Any promo message that must be added to end of caption.
            Set to None if no promo message to be added

        :returns:
        Caption to use in fediverse post
        """
        logger.debug(
            "RedditHelper.get_caption("
            "submission='%s', max_len=%s, add_hash_tags='%s', promo_message='%s')",
            submission.id,
            max_len,
            add_hash_tags,
            promo_message,
        )
        # Create string of hashtags
        hashtag_string = ""
        promo_string = ""
        hashtags_for_post = self.config.bot.hash_tags

        # Workout hashtags for post
        if add_hash_tags:
            hashtags_for_subreddit = [x.strip() for x in add_hash_tags.split(",")]
            hashtags_for_post = hashtags_for_subreddit + self.config.bot.hash_tags
        if hashtags_for_post:
            for tag in hashtags_for_post:
                # Add hashtag to string, followed by a space for the next one
                hashtag_string += "#" + tag + " "

        if promo_message:
            promo_string = f" \n \n{self.config.promo.message}"
        caption_max_length = max_len
        caption_max_length -= (
            len(submission.shortlink) - len(hashtag_string) - len(promo_string)
        )

        caption: str = ""
        # Create contents of the Mastodon post
        if len(submission.title) < caption_max_length:
            temp_caption = submission.title + " "
        else:
            temp_caption = submission.title[caption_max_length - 2] + "... "
        if self.config.mastodon_config.use_caption:
            caption += temp_caption
        if self.config.mastodon_config.use_tags:
            caption += hashtag_string
        if self.config.mastodon_config.use_backlink:
            if self.config.mastodon_config.link_to_media:
                caption += submission.url
            else:
                caption += submission.shortlink
        caption += promo_string
        return caption


class LinkedMediaHelper:
    """ImgurHelper provides methods to collect data / content from Imgur and
    Gfycat.
    """

    def __init__(
        self: LMH,
        config: Configuration,
        imgur_secrets: Secret,
    ) -> None:
        """Initialise LinkedMediaHelper instance.

        :param config: Configuration settings
        :param imgur_secrets: secrets to use with imgur api

        """
        self.save_dir = config.media.folder

        self.imgur_client = ImgurClient(
            client_id=imgur_secrets.client_id,
            client_secret=imgur_secrets.client_secret,
        )

    async def get_imgur_image(
        self: LMH, img_url: str, max_images: int = 4
    ) -> List[str]:
        """Download images from imgur.

        :param img_url: url of imgur image to download
        :param max_images: maximum number of images to download and process, Defaults to 4

        :returns:
        path to downloaded image or None if no image was downloaded
        """
        # Working demo of regex: https://regex101.com/r/G29uGl/2
        regex = r"(?:.*)imgur\.com(?:\/gallery\/|\/a\/|\/)(.*?)(?:\/.*|\.|$)"
        regex_match = re.search(regex, img_url, flags=0)

        if not regex_match:
            logger.error("Could not identify Imgur image/gallery ID at: %s", img_url)
            return []

        # Get the Imgur image/gallery ID
        imgur_id = regex_match.group(1)

        image_urls = self._get_image_urls(img_url, imgur_id)

        # Download and process individual images (up to max_images)
        imgur_paths: List[str] = []
        for url in image_urls:
            # If the URL is a GIFV or MP4 link, change it to the GIF version
            file_extension = os.path.splitext(url)[-1].lower()
            image_url = url
            if file_extension == ".gifv":
                file_extension = ".gif"
                image_url = url.replace(".gifv", ".gif")
            elif file_extension == ".mp4":
                file_extension = ".gif"
                image_url = url.replace(".mp4", ".gif")

            # Download the image
            file_path = (
                self.save_dir
                + "/"
                + imgur_id
                + "_"
                + str(len(imgur_paths))
                + file_extension
            )
            logger.debug(
                "Downloading Imgur image at URL %s to %s", image_url, file_path
            )
            saved_paths = await get_file(
                img_url=image_url,
                file_path=file_path,
                progress_label="Downloading Imgur image",
            )

            # Imgur will sometimes return a single-frame thumbnail
            # instead of a GIF, so we need to check for this
            if saved_paths and (
                file_extension != ".gif" or self._check_imgur_gif(saved_paths)
            ):
                imgur_paths.append(saved_paths)

            if len(imgur_paths) == max_images:
                break

        return imgur_paths

    def _get_image_urls(self: LMH, img_url: str, imgur_id: str) -> List[str]:
        """Build a list of urls of all Imgur images identified by imgur_id.

        :param img_url: URL to IMGUR post
        :param imgur_id: ID for IMGUR post

        :returns:
        imgur_urls: List of urls to images of Imgur post identified byr imgur_id
        """
        image_urls = []
        try:
            if any(s in img_url for s in ("/a/", "/gallery/")):  # Gallery links
                logger.debug("Imgur link points to gallery: %s", img_url)
                images = self.imgur_client.get_album_images(imgur_id)
                for image in images:
                    image_urls.append(image.link)
            else:  # Single image
                imgur_img = self.imgur_client.get_image(imgur_id)
                image_urls = [imgur_img.link]  # pylint: disable=no-member

        except ImgurClientError as imgur_error:
            logger.error("Could not get information from imgur: %s", imgur_error)
        return image_urls

    def _check_imgur_gif(self: LMH, file_path: str) -> bool:
        """Check if a file downloaded from imgur is indeed a gif. If file is not a gif, remove the file.

        :param file_path: file name and path to downloaded image

        :returns:
        True if downloaded image is indeed a GIF, otherwise returns False
        """
        mime = magic.from_file(filename=file_path, mime=True)
        if mime != "image/gif":
            logger.warning("Imgur: not a GIF, not posting")
            try:
                os.remove(file_path)
            except OSError as remove_error:
                logger.error("Error while deleting media file: %s", remove_error)
            return False

        return True

    def get_gfycat_image(self: LMH, img_url: str) -> Optional[str]:
        """Download full resolution images from gfycat.

        :param img_url: url of gfycat image to download

        :returns:
        file_path (string): path to downloaded image or None if no image was downloaded
        """
        logger.debug("LinkedMediaHelper.get_gfycat_image(img_url=%s)", img_url)

        saved_paths = LinkedMediaHelper._get_video_with_yt_dlp(
            video_url=img_url,
            save_as=self.save_dir + "/" + os.path.basename(urlsplit(img_url).path),
        )
        return saved_paths

    async def get_reddit_image(self: LMH, img_url: str) -> Optional[str]:
        """Download full resolution images from i.reddit or reddituploads.com.

        :param img_url (string): url of imgur image to download

        :returns:
        file_path (string): path to downloaded image or None if no image was downloaded
        """
        file_name = os.path.basename(urlsplit(img_url).path)
        file_extension = os.path.splitext(img_url)[1].lower()
        # Fix for issue with i.reddituploads.com links not having a
        # file extension in the URL
        if not file_extension:
            file_extension += ".jpg"
            file_name += ".jpg"
            img_url += ".jpg"
        # Download the file
        file_path = self.save_dir + "/" + file_name
        logger.debug(
            "Downloading file at URL %s to %s, file type identified as %s",
            img_url,
            file_path,
            file_extension,
        )

        saved_path = await get_file(
            img_url=img_url,
            file_path=file_path,
            progress_label="Downloading reddit image",
        )

        return saved_path

    async def get_reddit_gallery(
        self: LMH,
        reddit_post: Submission,
        max_images: int = 4,
    ) -> List[Optional[str]]:
        """Download up to max_images images from a reddit gallery post and returns a List of file_paths
        downloaded images.

        :param reddit_post:  reddit post / submission object
        :param max_images: [optional] maximum number of images to download. Default is 4

        :returns:
        file_paths (List[str]) a list of the paths to downloaded files. If no images have been downloaded, and empty
        list will be returned.
        """
        file_paths: List[Optional[str]] = []
        if reddit_post.gallery_data.get("items"):
            gallery_items: List[Dict[str, Any]] = reddit_post.gallery_data["items"]
            tasks: List[Any] = []
            for item in gallery_items:
                media_id = item["media_id"]
                meta = reddit_post.media_metadata[media_id]
                logger.debug("Media Metadata: %s", meta)
                if "e" in meta and meta["e"] == "Image":
                    source = meta["s"]
                    save_path = (
                        self.save_dir + "/" + media_id + "." + meta["m"].split("/")[1]
                    )
                    logger.debug(
                        "Gallery file_path, source: %s - %s", save_path, source["u"]
                    )
                    tasks.append(
                        get_file(source["u"], save_path, f"image {len(tasks)+1}")
                    )

                    if len(tasks) == max_images:
                        break

            print("Downloading images from reddit gallery")
            file_paths = await asyncio.gather(*tasks)

        return file_paths

    def get_reddit_video(self: LMH, reddit_post: Submission) -> Optional[str]:
        """Download full resolution video from i.reddit or reddituploads.

        :param reddit_post: reddit post / submission object

        :returns:
        file_path (string): path to downloaded video or None if no image was downloaded
        """
        logger.debug(
            "LinkedMediaHelper.get_reddit_video(reddit_post = %s)",
            reddit_post.id,
        )
        logger.debug(
            "LinkedMediaHelper.get_reddit_video - reddit_post.media: \n%s)",
            reddit_post.media,
        )

        # Download video with yt-dlp
        yt_dlp_url = reddit_post.media["reddit_video"]["hls_url"]
        print(f"Downloading Reddit video from {yt_dlp_url}")

        filepath = LinkedMediaHelper._get_video_with_yt_dlp(
            video_url=yt_dlp_url,
            save_as=self.save_dir + "/" + reddit_post.id,
        )
        return filepath

    @staticmethod
    def _get_video_with_yt_dlp(video_url: str, save_as: str) -> Optional[str]:
        """Download video files with embedded yt-dlp.

        :param video_url: URL for video to download
        :param save_as: path and file name excluding file extension for yt-dlp to
                download video file to

        :returns:
            (string) containing file name inclusive file extension and path where yt-dlp
                has saved the downloaded video.
                This can be None if yt-dlp has been unsuccessful.
        """
        logger.debug(
            "LinkedMediaHelper._get_video_with_yt_dlp(video_url=%s, save_as=%s)",
            video_url,
            save_as,
        )
        yt_dlp_options = {
            "outtmpl": save_as + ".%(ext)s",
            "quiet": "true",
            "ignoreerrors": "true",
            "progress": "true",
            "format": "bestvideo+bestaudio",
        }

        with yt_dlp.YoutubeDL(yt_dlp_options) as ytdl:
            meta = ytdl.extract_info(video_url, download=True)
            meta_san = ytdl.sanitize_info(meta)

        # If there was an error with yt-dlp download meta will be None
        if not meta:
            logger.debug(
                "LinkedMediaHelper.get_reddit_video - yt-dlp unsuccessful -> None"
            )
            return None

        yt_dlp_filepath: str = meta.get("filepath")
        if yt_dlp_filepath:
            logger.debug(
                "LinkedMediaHelper.get_reddit_video - yt-dlp DIRECT filepath: '%s'",
                yt_dlp_filepath,
            )
        else:
            yt_dlp_filepath = meta_san.get("requested_downloads")[0].get("filepath")
            logger.debug(
                "LinkedMediaHelper.get_reddit_video - yt-dlp 3 DEEP filepath: '%s'",
                yt_dlp_filepath,
            )
        logger.debug(
            "LinkedMediaHelper.get_reddit_video (...) -> '%s'", yt_dlp_filepath
        )

        return yt_dlp_filepath

    async def get_giphy_image(self: LMH, img_url: str) -> Optional[str]:
        """Download full or low resolution image from giphy.

        :param img_url: url of giphy image to download

        :returns:
        file_path (string): path to downloaded image or None if no image was downloaded
        """
        # Working demo of regex: https://regex101.com/r/o8m1kA/2
        regex = (
            r"https?://((?:.*)giphy\.com/media/|giphy.com"
            r"/gifs/|i.giphy.com/)(.*-)?(\w+)(/|\n)"
        )
        match = re.search(regex, img_url, flags=0)
        if not match:
            logger.error("Could not identify Giphy ID in this URL: %s", img_url)
            return None

        # Get the Giphy ID
        giphy_id = match.group(3)
        # Download the MP4 version of the GIF
        giphy_url = "https://media.giphy.com/media/" + giphy_id + "/giphy.mp4"
        file_path = self.save_dir + "/" + giphy_id + "giphy.mp4"

        saved_paths = await get_file(
            img_url=giphy_url,
            file_path=file_path,
            progress_label="Downloading Giphy image/video",
        )

        logger.debug("Downloaded Giphy at URL %s to %s", giphy_url, saved_paths)

        return saved_paths

    async def get_generic_image(self: LMH, img_url: str) -> Optional[str]:
        """Download image or video from a generic url to a media file.

        :param img_url: url to image or video file

        :returns:
        file_path (string): path to downloaded video or None if no image was downloaded
        """
        logger.debug("LinkedMediaHelper.get_generic_image(img_url=%s)", img_url)

        # First check if URL starts with http:// or https://
        regex = r"^https?://"
        match = re.search(regex, img_url, flags=0)
        if not match:
            logger.debug("Post link is not a full link: %s", img_url)
            return None

        # Check if URL is an image or MP4 file, based on the MIME type
        image_formats = (
            "image/png",
            "image/jpeg",
            "image/gif",
            "image/webp",
            "video/mp4",
        )

        try:
            async with aiohttp.ClientSession(
                raise_for_status=True,
                read_timeout=30,
            ) as client:
                response = await client.head(url=img_url)
                headers = response.headers
                content_type = headers.get("content-type", None)

        except (aiohttp.ClientError, asyncio.exceptions.TimeoutError) as error:
            logger.error("Error while opening URL: %s ", error)
            return None

        if content_type not in image_formats:
            logger.debug("URL does not point to a valid image file: %s", img_url)
            return None

        # URL appears to be an image, so download it
        file_name = os.path.basename(urlsplit(img_url).path)
        file_path = self.save_dir + "/" + file_name
        logger.debug("Downloading file at URL %s to %s", img_url, file_path)

        saved_path = await get_file(
            img_url=img_url,
            file_path=file_path,
            progress_label="Downloading generic image",
        )

        return saved_path


class MediaAttachment:
    """MediaAttachment contains code to retrieve the appropriate images or
    videos to include in a reddit post to be shared on Mastodon.
    """

    def __init__(
        self: MA, reddit_post: Submission, image_helper: LinkedMediaHelper
    ) -> None:
        """Initialise MediaAttachment instance.

        :param reddit_post: reddit post / submission
        :param image_helper: MediaHelper to deal with images or videos linked in reddit post
        """
        self.media_paths: Dict[str, str] = {}
        self.reddit_post = reddit_post
        self.media_url = self.reddit_post.url
        self.image_helper = image_helper

    async def get_media_files(self: MA) -> None:
        """Download media files linked to given reddit_post."""
        logger.debug("URL for post(%s): %s ", self.reddit_post, self.media_url)

        media_paths = await self.get_media()
        for media_path in media_paths:
            logger.debug("Media path for checksum calculation: %s", media_path)
            if media_path:
                sha256 = hashlib.sha256()
                async with aiofiles.open(file=media_path, mode="rb") as media_file:
                    # Read and update hash string value in blocks of 64K
                    while True:
                        data = await media_file.read(2**16)
                        if not data:
                            break
                        sha256.update(data)

                self.media_paths[sha256.hexdigest()] = media_path

    def destroy(self: MA) -> None:
        """Remove any files downloaded and clear out the object attributes."""
        try:
            for media_path in self.media_paths.values():
                if media_path is not None:
                    os.remove(media_path)
                    logger.debug("Deleted media file at %s", media_path)
        except OSError as delete_error:
            logger.error("Error while deleting media file: %s", delete_error)

        self.media_paths = {}
        self.media_url = None

    def destroy_one_attachment(self: MA, checksum: str) -> None:
        """Remove file with checksum downloaded.

        :param checksum: key to media_paths dictionary for file to be removed.
        """
        try:
            media_path = self.media_paths[checksum]
            if media_path is not None:
                os.remove(media_path)
                logger.debug("Deleted media file at %s", media_path)
            self.media_paths.pop(checksum)
        except OSError as delete_error:
            logger.error("Error while deleting media file: %s", delete_error)

    async def get_media(self: MA) -> List[Optional[str]]:
        """Determine which method to call depending on which site the media_url is pointing to.

        :returns:
        list of file-paths of downloaded images. Can be None
        """
        if not os.path.exists(self.image_helper.save_dir):
            os.makedirs(self.image_helper.save_dir)
            logger.debug(
                "Media folder not found, created new folder: %s",
                self.image_helper.save_dir,
            )

        file_paths = []
        saved_media_path: Optional[str]
        saved_media_paths: Iterable[Optional[str]]

        # Download and save the linked image
        if any(s in self.media_url for s in ("i.redd.it", "i.reddituploads.com")):
            saved_media_path = await self.image_helper.get_reddit_image(self.media_url)
            file_paths.append(saved_media_path)
        elif "v.redd.it" in self.media_url and not self.reddit_post.media:
            logger.error(
                "Reddit API returned no media for this URL: %s", self.media_url
            )
        elif "v.redd.it" in self.media_url:
            saved_media_path = self.image_helper.get_reddit_video(self.reddit_post)
            file_paths.append(saved_media_path)

        elif "imgur.com" in self.media_url:
            saved_media_paths = await self.image_helper.get_imgur_image(self.media_url)
            file_paths.extend(saved_media_paths)

        elif "gfycat.com" in self.media_url:
            saved_media_path = self.image_helper.get_gfycat_image(self.media_url)
            file_paths.append(saved_media_path)

        elif "giphy.com" in self.media_url:
            saved_media_path = await self.image_helper.get_giphy_image(self.media_url)
            file_paths.append(saved_media_path)

        elif "reddit.com/gallery/" in self.media_url:  # Need to check for gallery post
            if hasattr(self.reddit_post, "is_gallery"):
                logger.debug("%s is a gallery post", self.reddit_post.id)
                save_media_paths = await self.image_helper.get_reddit_gallery(
                    self.reddit_post
                )
                file_paths.extend(save_media_paths)

        else:
            saved_media_path = await self.image_helper.get_generic_image(self.media_url)
            file_paths.append(saved_media_path)

        return file_paths
