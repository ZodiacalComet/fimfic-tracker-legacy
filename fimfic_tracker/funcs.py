from datetime import datetime
from json import dump as json_dump

import click
import requests

from .config import DOWNLOAD_DIR, DOWNLOAD_FORMAT, TRACKER_FILE, EchoColor
from .constants import (
    CHARACTER_CONVERSION,
    FIMFIC_STORY_API_URL,
    ConfirmState,
    StoryStatus,
)


def get_story_data(story_id: str, *, do_echoes=True) -> dict:
    """Makes a request to the given Fimfiction story ID and extracts relevant
    data out of it.

    Arguments:
        story_id {str} -- ID of the story to get the data from.

    Keyword Arguments:
        do_echoes {bool} -- (default: {True})

    Returns:
        dict -- Story mapping of the following keys:
            - `title` {str} -- Title of the story.
            - `chapter-amt` {int} -- Amount of chapters the story has.
            - `words` {int} -- Amount of words the story has.
            - `last-update-timestamp` {float} -- Timestamp of the last update.
            - `completion-status` {int} -- StoryStatus enum value.
    """
    if do_echoes:
        click.secho(
            f"Extracting data from the story of ID {story_id}...", fg=EchoColor.info
        )

    req = requests.get(FIMFIC_STORY_API_URL, params={"story": story_id})
    story_data = req.json()["story"]

    return {
        "title": story_data["title"],
        "chapter-amt": len(story_data["chapters"]),
        "words": story_data["words"],
        "last-update-timestamp": story_data["date_modified"],
        "completion-status": StoryStatus.get_enum_from(story_data["status"]),
    }


def has_an_update(page_data: dict, tracker_data: dict) -> bool:
    """Checks if there was an update comparing two story mappings of the same
    story.

    Arguments:
        page_data {dict} -- Requested story mapping, from `get_story_data`.
        tracker_data {dict} -- Story mapping from the tracked list.

    Returns:
        bool -- Whether or not there was an update.
    """
    for key in ("words", "chapter-amt", "last-update-timestamp"):
        if page_data[key] > tracker_data[key]:
            return True

    return False


def get_size_str_from_bytes(size_bytes: int) -> str:
    """Returns a human readable representation of given bytes.

    Arguments:
        size_bytes {int} -- Size in bytes.

    Returns:
        str -- String representation of given bytes.
    """
    for i, suffix in enumerate(["b", "Kb", "Mb", "Gb", "Tb"]):
        size_bytes = size_bytes if i == 0 else (size_bytes / 1024)

        if not size_bytes > 900:
            break

    return f"{size_bytes:.2f} {suffix}"


def ljust_column_print(message: str, **kwargs):
    """Prints given message left-justified to terminal column size.

    Arguments:
        message {str} -- Message to print.

    Keyword Arguments:
        fg {str} -- Foreground to give to message with the click.style function.
        kwargs -- Keyword arguments to use on print.
    """
    fg = kwargs.pop("fg")
    if fg:
        message = click.style(message, fg=fg)

    print(message.ljust(click.get_terminal_size()[0] - 1), **kwargs)


def download_story(story_id: str, story_data: dict):
    """Download the story to the download directory given its ID and data.

    Arguments:
        story_id {dict} -- The ID of the story to download.
        story_data {dict} -- Data of the story to download.
    """
    download_url = DOWNLOAD_FORMAT["url_format"].format(STORY_ID=story_id)
    filename = (story_data["title"] + "." + DOWNLOAD_FORMAT["extension"]).translate(
        CHARACTER_CONVERSION
    )
    downloaded_bytes = 0

    # From: https://stackoverflow.com/a/16696317
    with requests.get(download_url, stream=True) as r:
        r.raise_for_status()
        with open(DOWNLOAD_DIR / filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
                downloaded_bytes += len(chunk)

                ljust_column_print(
                    f'Downloading "{filename}" [{get_size_str_from_bytes(downloaded_bytes)}]',
                    fg=EchoColor.info,
                    flush=True,
                    end="\r",
                )

    ljust_column_print(f'Saved as "{filename}"', fg=EchoColor.success)


def get_date_from_timestamp(timestamp: float) -> str:
    """Get a string representation of the date of the given timestamp.

    Arguments:
        timestamp {float} -- timestamp to get the date from.

    Returns:
        str -- The date in string form of the timestamp.
    """
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime("%d %h %Y")


def save_to_track_file(data: dict):
    """Save given data to the track file.

    Arguments:
        data {dict} -- Data to save to the track file.
    """
    with TRACKER_FILE.open("w", encoding="utf-8") as f:
        json_dump(data, f, ensure_ascii=False, indent=2)


def get_highlighted_value(value):
    """Returns the string representation of the given value highlighted.

    Arguments:
        value {Any} -- Value to highlight.

    Returns:
        str -- The highlighted string representation of the value.
    """

    def get_color(v):
        if isinstance(v, str):
            return EchoColor.hl_string
        elif isinstance(v, (int, float)):
            return EchoColor.hl_number
        return EchoColor.hl_fallback

    return click.style(str(value), fg=get_color(value))


def get_confirm_state(assume_yes: bool, assume_no: bool) -> ConfirmState:
    """Returns the state in which to manage the confirmation prompts from the
    assume flag values.

    Arguments:
        assume_yes {bool} -- Option flag value.
        assume_no {bool} -- Option flag value.

    Returns:
        ConfirmState -- The corresponding confirm state.
    """
    if assume_yes:
        return ConfirmState.answer_yes
    elif assume_no:
        return ConfirmState.answer_no
    else:
        return ConfirmState.prompt


def confirm(confirm_state: ConfirmState, confirm_msg: str) -> bool:
    """Checks for the confirm state to take into account the use of assume
    flags for confirmation prompts (yes/no questions). Allowing to
    automatically answer them if requested.

    To ensure that it works correctly, the confirm_state should be the result
    of the get_confirm_state function.

    Arguments:
        confirm_state {ConfirmState} -- Whether to prompt the user or
        automatically answer.
        confirm_msg {str} -- Question to ask should the confirm_state be of
        prompting the user.

    Returns:
        bool -- The answer to the confirmation prompt, with 'yes' being True
        and 'no' being False.
    """
    if confirm_state == ConfirmState.answer_yes:
        return True
    elif confirm_state == ConfirmState.answer_no:
        return False
    return click.confirm(confirm_msg)
