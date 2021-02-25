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

# If uncommented, this will be excuted as a command in the download process
# instead of directly downloading from Fimfiction.
# The command has to be given as a list of arguments, each of them can contain
# placeholders that will be replaced when downloading each story. Formatted as:
#       ${name} or $name
# Where $$ is a literal $.
# The names allowed are the following.
#   + id - The story id.
#   + title - The title of the story.
#   + safe_title - Story title but usable as a filename.
#   + author - The name of the author of the story.
#   + safe_author - Story author's name but usable as a filename.
#   + chapter_amt - The amount of chapters the story has.
#   + words - The amount of words the story has.
#   + last_update_timestamp - A number that represents the timestamp of the last
#     update that the story had.
#   + completion_status - A number that represents the status of the story. Being:
#         0 - Complete
#         1 - Incomplete
#         2 - On Hiatus
#         3 - Cancelled
# Type: list
# download_alt = []
#
# Examples:
#
# + Alternative download method
# download_alt = [
#     "wget",
#     "-O", download_dir / "${safe_title}.html",
#     "https://www.fimfiction.net/story/download/$id/html"
# ]
#
# + For the EPUB format provided by fimfic2epub
#   https://github.com/daniel-j/fimfic2epub
#
# download_alt = ["fimfic2epub", "--dir", download_dir, "$id"]
# If you installed it on Windows, use the one below instead.
# download_alt = ["fimfic2epub.cmd", "--dir", download_dir, "$id"]
#
# + For the EPUB format provided by FanFicFare
#   https://github.com/JimmXinu/FanFicFare
#
# output_filename = download_dir / "$${title}-$${siteabbrev}_$${storyId}$${formatext}"
# download_alt = [
#     "fanficfare",
#     "-f", "epub",
#     "-u",
#     "--non-interactive",
#     "--update-cover",
#     "--option", f"output_filename={output_filename}",
#     "--option", "include_images=true",
#     "https://www.fimfiction.net/story/$id"
# ]

# Whether or not to supress the output of the command defined in download_alt.
# Type: bool
download_alt_quiet = True

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
