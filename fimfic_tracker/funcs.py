from datetime import datetime
from json import dump as json_dump

import click
import requests
from bs4 import BeautifulSoup
from dateparser import parse as dateparser_parse

from .config import DOWNLOAD_DIR, DOWNLOAD_FORMAT, TRACKER_FILE, EchoColor
from .constants import CHARACTER_CONVERSION, FIMFIC_BASE_URL, STATUS_CLASS_NAMES


def get_story_data(url: str, *, do_echoes=True) -> dict:
    """Makes a request to the given Fimfiction story URL and extracts relevant
    data out of it.

    Arguments:
        url {str} -- URL of the story to get the data from.

    Keyword Arguments:
        do_echoes {bool} -- (default: {True})

    Returns:
        dict -- Story mapping of the following keys:
            - `title` {str} -- Title of the story.
            - `url` {str} -- Fimfiction URL.
            - `chapter-amt` {int} -- Amount of chapters the story has.
            - `last-update-timestamp` {float} -- Timestamp of the last update.
            - `download-url` {str} -- Story download URL.
            - `completion-status` {int} -- StoryStatus enum value.
    """
    if do_echoes:
        click.secho(f'Making a request to "{url}"', fg=EchoColor.info)

    cookies = dict(view_mature="true")
    page_content = requests.get(url, cookies=cookies).content

    if do_echoes:
        click.secho("Extracting data...", fg=EchoColor.info)

    soup = BeautifulSoup(page_content, "lxml")

    story_container = soup.find("article", class_="story_container")

    chapter_list = story_container.find("ul", class_="chapters")
    chapters = chapter_list.find_all("li", recursive=False)

    filter_expander = filter(
        lambda li: not li.find("div", class_="chapter_expander"), chapters
    )

    chapters = list(filter_expander)

    def get_story_name() -> str:
        story_name = story_container.find("a", class_="story_name")
        return story_name.text.strip()

    def get_timestamp_from_chapter(ch) -> float:
        date = ch.find("span", class_="date")
        mobile = date.find("span", class_="mobile")

        date_string = date.text[2 : -len(mobile.text)]
        return dateparser_parse(date_string, languages=["en"]).timestamp()

    def get_download_url() -> str:
        download = story_container.find("span", class_="download")
        for download in download.ul.find_all("a"):
            if DOWNLOAD_FORMAT not in download.text:
                continue

            return FIMFIC_BASE_URL + download["href"]

    def get_status() -> int:
        for class_name, status in STATUS_CLASS_NAMES.items():
            if story_container.find("span", class_=class_name):
                return status.value

    return {
        "title": get_story_name(),
        "url": url,
        "chapter-amt": len(chapters),
        "last-update-timestamp": max(map(get_timestamp_from_chapter, chapters)),
        "download-url": get_download_url(),
        "completion-status": get_status(),
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
    for key in ("chapter-amt", "last-update-timestamp"):
        if page_data[key] > tracker_data[key]:
            return True

    return False


def download_story(story_data: dict):
    """Download the story with the given data to the download directory.

    Arguments:
        story_data {dict} -- Data of the story to download.
    """
    click.secho("Downloading story...", fg=EchoColor.info)
    filename = (story_data["title"] + DOWNLOAD_FORMAT).translate(CHARACTER_CONVERSION)

    # From: https://stackoverflow.com/a/16696317
    with requests.get(story_data["download-url"], stream=True) as r:
        r.raise_for_status()
        with open(DOWNLOAD_DIR / filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    click.secho(f'Saved as "{filename}"', fg=EchoColor.success)


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
