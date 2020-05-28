from enum import Enum
from os import getenv
from pathlib import Path

DEFAULT_TRACKER_DIR = Path.home() / ".fimfic-tracker"
ENV_TRACKER_DIR = getenv("FIMFIC_TRACKER_DIR")

FIMFIC_TRACKER_DIR = Path(ENV_TRACKER_DIR) if ENV_TRACKER_DIR else DEFAULT_TRACKER_DIR

DOWNLOAD_DIR = FIMFIC_TRACKER_DIR / "downloads"
TRAKER_FILE = FIMFIC_TRACKER_DIR / "track-data.json"

FIMFIC_BASE_URL = "https://www.fimfiction.net"

DOWNLOAD_FORMAT = ".txt"
DOWNLOAD_DELAY = 1

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


# Color Names: https://click.palletsprojects.com/en/7.x/api/#click.style
class EchoColor:
    info = "bright_cyan"
    success = "bright_green"
    error = "bright_red"

    confirm_prompt = "bright_white"

    # Value Highlights
    hl_string = "bright_green"
    hl_number = "bright_blue"
    hl_fallback = "bright_white"
