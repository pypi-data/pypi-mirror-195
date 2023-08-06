"""Package 'tootbot' level definitions."""
import sys
from typing import Final

__version__: Final[str] = "7.0.3"
__display_name__: Final[str] = "Tootbot"
__package_name__: Final[str] = __display_name__.lower()

# Package level Static Variables
POST_RECORDER_SQLITE_DB: Final[str] = "history.db"
USER_AGENT: Final[str] = __display_name__
CLIENT_WEBSITE: Final[str] = "https://pypi.org/project/tootbot/"
PROGRESS_BAR_FORMAT: Final[
    str
] = "{desc}: {percentage:3.0f}%|{bar}| Eta: {remaining} - Elapsed: {elapsed}"
FATAL_TOOTBOT_ERROR: Final[str] = "Tootbot cannot continue, now shutting down"
VERSION_DEBUG: Final[
    str
] = f"{__display_name__}_{__version__}_Python_{sys.version.split()[0]}"
