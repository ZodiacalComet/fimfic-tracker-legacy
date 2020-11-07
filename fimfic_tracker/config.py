import sys
from pathlib import Path

from .constants import VALID_DOWNLOAD_FORMATS, VALID_ECHO_COLORS

DEFAULT_TRACKER_DIR = Path.home() / ".fimfic-tracker"
CONFIG_FILE_LOCATIONS = [
    Path.home() / ".config" / "fimfic-tracker",
    DEFAULT_TRACKER_DIR,
]

INVALID_SETTING_TYPE_MSG = "{0} can only be one of the following: {1}."

for path in reversed(CONFIG_FILE_LOCATIONS):
    sys.path.insert(0, str(path))

try:
    import settings
except ModuleNotFoundError:
    settings = None


def get_value(name, default, value_type):
    attr = getattr(settings, name, default)

    if not isinstance(attr, value_type):
        expected_types = (
            " or ".join(map(lambda t: repr(t.__name__), value_type))
            if isinstance(value_type, tuple)
            else repr(value_type.__name__)
        )

        raise ValueError(
            "{0} expected value of type {1} but got '{2}' from the settings file.".format(
                name, expected_types, type(attr).__name__
            )
        )

    return attr


def get_echo_color(name, default):
    value = get_value(name, default, str)

    if value not in VALID_ECHO_COLORS:
        raise ValueError(
            INVALID_SETTING_TYPE_MSG.format(
                name, ",".join(map(repr, VALID_ECHO_COLORS))
            )
        )

    return value


DOWNLOAD_DIR = get_value("DOWNLOAD_DIR", DEFAULT_TRACKER_DIR / "downloads", Path)
TRACKER_FILE = get_value("TRACKER_FILE", DEFAULT_TRACKER_DIR / "track-data.json", Path)

DOWNLOAD_FORMAT = get_value("DOWNLOAD_FORMAT", ".txt", str)

if DOWNLOAD_FORMAT not in VALID_DOWNLOAD_FORMATS:
    raise ValueError(
        INVALID_SETTING_TYPE_MSG.format(
            "DOWNLOAD_FORMAT", ", ".join(map(repr, VALID_DOWNLOAD_FORMATS))
        )
    )

DOWNLOAD_DELAY = get_value("DOWNLOAD_DELAY", 1, (int, float))


class EchoColor:
    info = get_echo_color("INFO_FG_COLOR", "bright_cyan")
    success = get_echo_color("SUCCESS_FG_COLOR", "bright_green")
    error = get_echo_color("ERROR_FG_COLOR", "bright_red")

    confirm_prompt = get_echo_color("CONFIRM_FG_COLOR", "bright_white")

    # Value Highlights
    hl_string = get_echo_color("HIGHLIGHT_TEXT_COLOR", "bright_green")
    hl_number = get_echo_color("HIGHLIGHT_NUMBER_COLOR", "bright_blue")
    hl_fallback = get_echo_color("HIGHLIGHT_OTHER_COLOR", "bright_white")
