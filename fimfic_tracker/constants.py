from enum import Enum

FIMFIC_BASE_URL = "https://www.fimfiction.net"
FIMFIC_STORY_URL_REGEX = r"https?://(?:www.)?fimfiction.net/story/(?P<STORY_ID>\d+)"

KEYWORDS_TO_HIDE_ON_LIST = ["last-update-timestamp", "completion-status"]
# Doesn't seem like they will change anytime soon, so hardcoded they are!
# Also avoids the little case where get_download_url doesn't return
# anything. (funcs.py:65)
VALID_DOWNLOAD_FORMATS = [".txt", ".html", ".epub"]
# https://click.palletsprojects.com/en/7.x/api/#click.style
VALID_ECHO_COLORS = [
    "black",
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "white",
    "bright_black",
    "bright_red",
    "bright_green",
    "bright_yellow",
    "bright_blue",
    "bright_magenta",
    "bright_cyan",
    "bright_white",
    "reset",
]


class StoryStatus(Enum):
    completed = 0
    incomplete = 1
    on_hiatus = 2
    cancelled = 3


CHARACTER_CONVERSION = {ord(c): "_" for c in '><:"|?*'}

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
