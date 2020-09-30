import sys
from enum import Enum
from pathlib import Path

FIMFIC_TRACKER_DIR = Path.home() / ".fimfic-tracker"
FIMFIC_BASE_URL = "https://www.fimfiction.net"

KEYWORDS_TO_HIDE_ON_LIST = ["last-update-timestamp", "completion-status"]


class StoryStatus(Enum):
    completed = 0
    incomplete = 1
    on_hiatus = 2
    cancelled = 3


VALUE_TO_STATUS_NAME = {
    k: v.replace("_", " ").title()
    for k, v in map(lambda e: (e.value, e.name), StoryStatus)
}


STATUS_CLASS_NAMES = {
    "completed-status-complete": StoryStatus.completed,
    "completed-status-incomplete": StoryStatus.incomplete,
    "completed-status-hiatus": StoryStatus.on_hiatus,
    "completed-status-cancelled": StoryStatus.cancelled,
}


CHARACTER_CONVERSION = {ord(c): "_" for c in '><:"|?*'}

# Configurable values

CONFIG_FILE_LOCATIONS = [Path.home() / ".config" / "fimfic-tracker", FIMFIC_TRACKER_DIR]

for path in reversed(CONFIG_FILE_LOCATIONS):
    sys.path.insert(0, str(path))

try:
    import settings
except ModuleNotFoundError:
    settings = None

DOWNLOAD_DIR = getattr(settings, "DOWNLOAD_DIR", FIMFIC_TRACKER_DIR / "downloads")
TRACKER_FILE = getattr(settings, "TRACKER_FILE", FIMFIC_TRACKER_DIR / "track-data.json")

DOWNLOAD_FORMAT = getattr(settings, "DOWNLOAD_FORMAT", ".txt")
DOWNLOAD_DELAY = getattr(settings, "DOWNLOAD_DELAY", 1)


# Color Names: https://click.palletsprojects.com/en/7.x/api/#click.style
class EchoColor:
    info = getattr(settings, "INFO_FG_COLOR", "bright_cyan")
    success = getattr(settings, "SUCCESS_FG_COLOR", "bright_green")
    error = getattr(settings, "ERROR_FG_COLOR", "bright_red")

    confirm_prompt = getattr(settings, "CONFIRM_FG_COLOR", "bright_white")

    # Value Highlights
    hl_string = getattr(settings, "HIGHLIGHT_TEXT_COLOR", "bright_green")
    hl_number = getattr(settings, "HIGHLIGHT_NUMBER_COLOR", "bright_blue")
    hl_fallback = getattr(settings, "HIGHLIGHT_OTHER_COLOR", "bright_white")
