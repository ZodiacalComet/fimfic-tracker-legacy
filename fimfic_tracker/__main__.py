import json
import re
from time import sleep

import click

from .confreader import load_config
from .constants import (
    CONFIG_FILE_LOCATIONS,
    FIMFIC_STORY_URL_REGEX,
    KEYWORDS_TO_HIDE_ON_LIST,
    ConfirmState,
    StoryStatus,
)
from .exceptions import DownloadError
from .funcs import (
    confirm,
    download_story,
    get_confirm_state,
    get_date_from_timestamp,
    get_highlighted_value,
    get_story_data,
    has_an_update,
    save_to_track_file,
)


@click.group()
@click.version_option()
@click.option(
    "--config",
    "-c",
    metavar="CONFIG",
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
    help="Config file to load over every other one.",
)
@click.pass_context
def main(ctx, config):
    """An unnecessary CLI application for tracking Fimfiction stories."""
    from pathlib import Path

    ctx.ensure_object(dict)
    ctx.obj["config"] = config = load_config(
        CONFIG_FILE_LOCATIONS + ([Path(config)] if config else [])
    )

    download_dir = config["download_dir"]
    if not download_dir.exists():
        download_dir.mkdir(parents=True)

    tracker_file = config["tracker_file"]
    if not tracker_file.exists():
        if not tracker_file.parent.exists():
            tracker_file.parent.mkdir(parents=True)

        save_to_track_file({}, config)

    with tracker_file.open("r") as f:
        ctx.obj["track-data"] = json.load(f)


@main.command(short_help="Tracks stories and downloads them.")
@click.argument("urls", nargs=-1)
@click.option("--skip-download", "-s", is_flag=True)
@click.option(
    "--overwrite",
    "-o",
    is_flag=True,
    help="Automatically answers the overwrite prompts with Y.",
)
@click.pass_context
def track(ctx, urls, skip_download, overwrite):
    """Adds the given story URLs to the tracking list and downloads them to the
    download folder.

    If it is already tracked, you will be asked if you want to overwrite it."""
    config = ctx.obj["config"]

    for url in urls:
        match = re.match(FIMFIC_STORY_URL_REGEX, url)

        if not match:
            click.secho(
                f'"{url}" doesn\'t seem like an URL from a Fimfiction story.',
                err=True,
                fg=config["error_fg_color"],
            )
            continue

        story_id = match.groupdict()["STORY_ID"]
        if not overwrite and story_id in ctx.obj["track-data"]:
            title = ctx.obj["track-data"][story_id]["title"]
            msg = click.style(
                f'You already have the story "{title}" ({story_id}) on the tracking list. '
                "Do you want to overwrite it?",
                fg=config["confirm_fg_color"],
            )
            if not click.confirm(msg):
                click.secho("Skipping story.", fg=config["info_fg_color"])
                continue

        try:
            data = get_story_data(story_id, config)
        except DownloadError as err:
            click.secho(
                f"Couldn't get data from story of ID {story_id}.\n{err}\n",
                err=True,
                fg=config["error_fg_color"],
            )
            continue

        if not skip_download:
            try:
                download_story(story_id, data, config)
            except DownloadError as err:
                click.secho(
                    f"Couldn't download story.\n{err}\n",
                    err=True,
                    fg=config["error_fg_color"],
                )
                continue

        ctx.obj["track-data"][story_id] = data
        save_to_track_file(ctx.obj["track-data"], config)

        click.secho(
            f'"{data["title"]}" ({story_id}) has been added to the tracking list.',
            fg=config["success_fg_color"],
        )
        click.echo()


@main.command(short_help="Untracks stories.")
@click.argument("story-ids", nargs=-1)
@click.pass_context
def untrack(ctx, story_ids):
    """Removes the stories of the given STORY_IDS from the tracking list if
    they exist."""
    config = ctx.obj["config"]

    for story_id in story_ids:
        if story_id not in ctx.obj["track-data"]:
            click.secho(
                f"There is no story of ID {story_id} on the tracking list.",
                err=True,
                fg=config["error_fg_color"],
            )
            continue

        title = ctx.obj["track-data"][story_id]["title"]
        del ctx.obj["track-data"][story_id]

        save_to_track_file(ctx.obj["track-data"], config)

        click.secho(
            f'Successfully removed "{title}" ({story_id}) from the tracking list.',
            fg=config["success_fg_color"],
        )


@main.command("list")
@click.option("--short", "-s", is_flag=True, help="Show only the story ID and title.")
@click.pass_context
def _list(ctx, short):
    """List all tracked stories."""
    config = ctx.obj["config"]

    if not ctx.obj["track-data"]:
        click.secho(
            "There are no tracked stories.", err=True, fg=config["error_fg_color"]
        )
        return

    if short:
        for story_id, tracker_data in ctx.obj["track-data"].items():
            click.secho(
                "{0} {1}".format(
                    click.style(f"[{story_id}]", fg="bright_cyan"),
                    click.style(
                        tracker_data["title"], fg=config["highlight_text_color"]
                    ),
                )
            )
        return

    def echo_value(items):
        k = click.style(items[0], fg="bright_white")
        v = get_highlighted_value(items[1], config)
        click.echo(f"{k} = {v}")

    for story_id, tracker_data in ctx.obj["track-data"].items():
        click.secho(f"[ID {story_id}]", fg="bright_cyan")
        echo_value(
            [
                "last-update-date",
                get_date_from_timestamp(tracker_data["last-update-timestamp"]),
            ]
        )

        for items in filter(
            lambda i: i[0] not in KEYWORDS_TO_HIDE_ON_LIST, tracker_data.items()
        ):
            echo_value(items)

        echo_value(
            [
                "completion-status",
                StoryStatus.get_name_from(tracker_data["completion-status"]),
            ]
        )

        click.echo()


@main.command()
@click.option("--force", "-f", is_flag=True, help="Force download all tracked stories.")
@click.option(
    "--assume-yes",
    "-y",
    is_flag=True,
    help="Automatically answers confirmation prompts with Y.",
)
@click.option(
    "--assume-no",
    "-n",
    is_flag=True,
    help="Automatically answers confirmation prompts with N.",
)
@click.argument("story-ids", nargs=-1)
@click.pass_context
def download(ctx, force, assume_yes, assume_no, story_ids):
    """Download all or given STORY_IDS of tracked stories that have updated.

    If a story is registered as any status other than 'Incomplete', you will be
    asked if you still want to check for an update on it."""
    config = ctx.obj["config"]

    if not ctx.obj["track-data"]:
        click.secho(
            "There are no tracked stories.", err=True, fg=config["error_fg_color"]
        )
        return

    if assume_yes and assume_no:
        click.secho(
            'The options "--assume-yes" and "--assume-no" cannot be used at the same time.',
            err=True,
            fg=config["error_fg_color"],
        )
        return
    if force and (assume_yes or assume_no):
        click.secho(
            'The option "--force" is not compatible with "--assume-yes" nor "--assume-no".',
            err=True,
            fg=config["error_fg_color"],
        )
        return

    confirm_state = get_confirm_state(assume_yes, assume_no)

    def true_or_filter_ids(id_str: str) -> bool:
        if not story_ids:
            return True
        return id_str in story_ids

    for story_id, tracker_data in filter(
        lambda t: true_or_filter_ids(t[0]), ctx.obj["track-data"].items()
    ):
        title = tracker_data["title"]
        if not force:
            if not tracker_data["completion-status"] == StoryStatus.incomplete:
                status = StoryStatus.get_name_from(tracker_data["completion-status"])

                msg = click.style(
                    f'"{title}" ({story_id}) has been marked as "{status}" by the '
                    "author. Do you want to still check for an update on it?",
                    fg=config["confirm_fg_color"],
                )
                if not confirm(confirm_state, msg):
                    if confirm_state == ConfirmState.answer_no:
                        click.secho(
                            f'Skipping "{title}" ({story_id}) marked as "{status}".',
                            fg=config["info_fg_color"],
                        )
                    else:
                        click.secho("Skipping story.", fg=config["info_fg_color"])

                    click.echo()
                    continue

        click.secho(
            f'Checking if "{title}" ({story_id}) had an update...',
            fg=config["info_fg_color"],
        )

        try:
            page_data = get_story_data(story_id, config, do_echoes=False)
        except DownloadError as err:
            click.secho(
                f"Couldn't check for story.\n{err}\n",
                err=True,
                fg=config["error_fg_color"],
            )
            continue

        if not has_an_update(page_data, tracker_data):
            click.secho("Story didn't have an update.", fg="bright_yellow")

            if force:
                click.secho("Force downloading story.", fg="bright_yellow")
            elif not force:
                click.echo()
                continue

        try:
            download_story(story_id, page_data, config)
        except DownloadError as err:
            click.secho(
                f"Couldn't download story.\n{err}\n",
                err=True,
                fg=config["error_fg_color"],
            )
        else:
            ctx.obj["track-data"][story_id] = page_data
            save_to_track_file(ctx.obj["track-data"], config)

        click.echo()
        sleep(config["download_delay"])


if __name__ == "__main__":
    main(obj={})
