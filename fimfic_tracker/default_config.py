from pathlib import Path

# --- Paths
# Path to a directory in which to save the downloaded stories.
# Type: Path
download_dir = Path.home() / ".fimfic-tracker" / "downloads"

# Path to store the tracker file.
# Type: Path
tracker_file = Path.home() / ".fimfic-tracker" / "track-data.json"

# --- Download
# The format in which to download the stories. The valid values are:
# + "txt"
# + "html"
# + "epub"
# Type: str
download_format = "html"

# The seconds to wait before advancing to the next story.
# Type: int or float
download_delay = 1

# --- Colors
# The color to use for text in certain output. The list of valid values can be
# found at: https://click.palletsprojects.com/en/7.x/api/#click.style
# All of them are of type str.

info_fg_color = "bright_cyan"
success_fg_color = "bright_green"
error_fg_color = "bright_red"
confirm_fg_color = "bright_white"

highlight_text_color = "bright_green"
highlight_number_color = "bright_blue"
highlight_other_color = "bright_white"
