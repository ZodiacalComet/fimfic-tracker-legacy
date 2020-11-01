# fimfic-tracker

An unnecessary CLI application for tracking stories on [**Fimfiction**](https://www.fimfiction.net/). Because I'm weird and needed an easy way to track some stories without using my account.

Since it's working for me well enough, and that I really had a ton of fun making it, I thought: *Why not share it?*

<p align="center"><img src="https://i.imgur.com/uLHq3Jh.png"></p>

<p align="center">
<strong>
<a href="#installation">Installation</a>
·
<a href="#usage">Usage</a>
·
<a href="#configuration">Configuration</a>
·
<a href="#acknowledgments">Acknowledgments</a>
·
<a href="#license">License</a>
</strong>
</p>

## Installation

**Having Python installed is required, at least the 3.7 version.**

Use **pip** to install this project to your system.

```text
# Windows
python -m pip install git+https://github.com/ZodiacalComet/fimfic-tracker.git

# Linux
python3 -m pip install git+https://github.com/ZodiacalComet/fimfic-tracker.git
```

Or you can use [**pipx**](https://github.com/pipxproject/pipx#install-pipx) instead, which is my personal preference for this kind of Python applications.

```text
pipx install git+https://github.com/ZodiacalComet/fimfic-tracker.git
```

Alternately, you could clone this repository with git and install it locally.

```text
git clone https://github.com/ZodiacalComet/fimfic-tracker.git
cd fimfic-tracker

# With pip
python3 -m pip install .

# With pipx
pipx install -e .
```

## Usage

First thing to do is add a story to the tracking list, since there is none at this point, you use the `track` command like so:

<p align="center"><img src="https://i.imgur.com/BHa6Nr9.png"></p>

It accepts an unlimited amount of arguments, which means that you can add multiple stories to the tracking list at the same time.

<p align="center"><img src="https://i.imgur.com/3xPVbHK.png"></p>

Now that you have some stories tracked, you can use the `download` command anytime to check for updates:

<p align="center"><img src="https://i.imgur.com/feolL9v.png"></p>

The downloaded files end up by default in `~/.fimfic-tracker/downloads`.

> Use with moderation, since the most probable you will end up making a lot of requests to the page for each use.

Want to stop tracking a story for whatever reason? You need the ID of the story, which can be seen with the `list` command:

<p align="center"><img src="https://i.imgur.com/uWAfXcu.png"></p>

Now knowing the ID you use the `untrack` command and, like with the `track` command, you can specify more than one at once:

<p align="center"><img src="https://i.imgur.com/7bLICcM.png"></p>

## Configuration

The application searches for a `settings.py` file inside `~/.config/fimfic-tracker` and then in `~/.fimfic-tracker`.

Copy the following template, uncomment and edit to your preferences.

```py
#from pathlib import Path

## Paths
# Path to a directory in which to save the downloaded stories.
# Type: Path
#DOWNLOAD_DIR = Path.home() / ".fimfic-tracker" / "downloads"

# Path to store the tracker file.
# Type: Path
#TRACKER_FILE = Path.home() / ".fimfic-tracker" / "track-data.json"

## Download
# The format in which to download the stories. The valid values are:
# + ".txt"
# + ".html"
# + ".epub"
# Type: str
#DOWNLOAD_FORMAT = ".txt"

# The seconds to wait before advancing to the next story.
# Type: int or float
#DOWNLOAD_DELAY = 1

## Colors
# The color to use for text in certain output. The list of valid values can be
# found at: https://click.palletsprojects.com/en/7.x/api/#click.style
# All of them are of type str.

#INFO_FG_COLOR = "bright_cyan"
#SUCCESS_FG_COLOR = "bright_green"
#ERROR_FG_COLOR = "bright_red"
#CONFIRM_FG_COLOR = "bright_white"

#HIGHLIGHT_TEXT_COLOR = "bright_green"
#HIGHLIGHT_NUMBER_COLOR = "bright_blue"
#HIGHLIGHT_OTHER_COLOR = "bright_white"
```

## Acknowledgments

To these other projects, that made this one less of a headache to make!

- [**BeautifulSoup4**](https://launchpad.net/beautifulsoup): A program designed for screen-scraping HTML.
- [**Colorama**](https://github.com/tartley/colorama): Simple cross-platform colored terminal text in Python.
- [**Click**](https://github.com/pallets/click): Python composable command line interface toolkit.
- [**Dateparser**](https://github.com/scrapinghub/dateparser): python parser for human readable dates.
- [**lxml**](https://github.com/lxml/lxml): The lxml XML toolkit for Python.
- [**Requests**](https://github.com/psf/requests): A simple, yet elegant HTTP library.

And to [**Carbon**](https://carbon.now.sh/) for allowing me to make this README a little nicer to look at.

## License

This simple project is made public under the Unlicense License. So do whateverer you want with it.
