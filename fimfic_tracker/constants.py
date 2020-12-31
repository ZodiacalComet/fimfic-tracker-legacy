from enum import Enum

FIMFIC_BASE_URL = "https://www.fimfiction.net"
FIMFIC_STORY_API_URL = FIMFIC_BASE_URL + "/api/story.php"
FIMFIC_STORY_URL_REGEX = r"https?://(?:www.)?fimfiction.net/story/(?P<STORY_ID>\d+)"

KEYWORDS_TO_HIDE_ON_LIST = ["last-update-timestamp", "completion-status"]
# Doesn't seem like these URLs will change anytime soon if not never.
# So hardcoded they are!
DOWNLOAD_URL_BY_FORMAT = {
    extension: FIMFIC_BASE_URL + "/story/download/{STORY_ID}/" + extension
    for extension in ("txt", "html", "epub")
}

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


CHARACTER_CONVERSION = {ord(c): "_" for c in '><:"|?*'}


class ConfirmState(Enum):
    prompt = 0
    answer_yes = 1
    answer_no = 2


class StoryStatus:
    completed = 0
    incomplete = 1
    on_hiatus = 2
    cancelled = 3

    MAP = {
        completed: "Complete",
        incomplete: "Incomplete",
        on_hiatus: "On Hiatus",
        cancelled: "Cancelled",
    }

    def get_enum_from(self, name) -> int:
        for key, value in self.MAP.items():
            if value.casefold() == name.casefold():
                return key

    def get_name_from(self, enum) -> str:
        return self.MAP.get(enum)


StoryStatus = StoryStatus()
