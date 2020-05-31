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
<a href="#acknowledgements">Acknowledgements</a>
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

> As said in the main help, the application's directory is located at `~/.fimfic-tracker`. If you prefer it to be on another directory you should define it in the `FIMFIC_TRACKER_DIR` environment variable before starting.

First thing to do is add a story to the tracking list, since there is none at this point, you use the `track` command like so:

<p align="center"><img src="https://i.imgur.com/BHa6Nr9.png"></p>

It accepts an unlimited amount of arguments, which means that you can add multiple stories to the tracking list at the same time.

<p align="center"><img src="https://i.imgur.com/3xPVbHK.png"></p>

The downloaded files end up in `~/.fimfic-tracker/downloads`

> If you want it to be downloaded on a different format, `.html` or `.epub`, you have to modify this [line](https://github.com/ZodiacalComet/fimfic-tracker/blob/master/fimfic_tracker/constants.py#L15).

Now that you have some stories tracked, you can use the `download` command anytime to check for updates:

<p align="center"><img src="https://i.imgur.com/feolL9v.png"></p>

> Use with moderation, since the most probable you will end up making a lot of requests to page for each use.

Want to stop tracking a story for whatever reason? You need the ID of the story, which can be seen with the `list` command:

<p align="center"><img src="https://i.imgur.com/uWAfXcu.png"></p>

Now knowing the ID you use the `untrack` command and, like with the `track` command, you can specify more than one at once:

<p align="center"><img src="https://i.imgur.com/7bLICcM.png"></p>

## Acknowledgements

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
