import json
from time import sleep

import click

from .constants import (
    DOWNLOAD_DELAY,
    DOWNLOAD_DIR,
    FIMFIC_BASE_URL,
    FIMFIC_TRACKER_DIR,
    KEYWORDS_TO_HIDE_ON_LIST,
    TRAKER_FILE,
    VALUE_TO_STATUS_NAME,
    EchoColor,
    StoryStatus,
)
from .funcs import (
    download_story,
    get_date_from_timestamp,
    get_highlighted_value,
    get_story_data,
    has_an_update,
    save_to_track_file,
)


@click.group()
@click.version_option()
@click.pass_context
def main(ctx):
    """An unnecessary CLI application for tracking Fimfiction stories.

    By default "~/.fimfic-tracker" is the application's directory. It can
    be changed with the FIMFIC_TRACKER_DIR environment variable.

    Downloads are made in a "downloads" directory inside the application's
    directory."""
    if not FIMFIC_TRACKER_DIR.exists():
        FIMFIC_TRACKER_DIR.mkdir(parents=True)

    if not DOWNLOAD_DIR.exists():
        DOWNLOAD_DIR.mkdir(parents=True)

    if not TRAKER_FILE.exists():
        TRAKER_FILE.touch()

        save_to_track_file({})

    ctx.ensure_object(dict)

    with TRAKER_FILE.open("r") as f:
        ctx.obj["track-data"] = json.load(f)


@main.command(short_help="Tracks stories and downloads them.")
@click.argument("urls", nargs=-1)
@click.option("--skip-download", is_flag=True)
@click.pass_context
def track(ctx, urls, skip_download):
    """Adds the given story URLs to the tracking list and downloads them to the
    download folder.

    If it is already tracked, you will be asked if you want to overwrite it."""
    for url in urls:
        if not url.startswith(f"{FIMFIC_BASE_URL}/story/"):
            click.secho(
                f'"{url}" doesn\'t seem like an URL from Fimfiction.',
                fg=EchoColor.error,
            )
            continue

        story_id = url.split("/")[-2]
        if story_id in ctx.obj["track-data"]:
            title = ctx.obj["track-data"][story_id]["title"]
            msg = click.style(
                f'You already have the story "{title}" ({story_id}) on the tracked list. '
                "Do you want to overwrite it?",
                fg=EchoColor.confirm_prompt,
            )
            if not click.confirm(msg):
                click.secho("Skipping story.", fg=EchoColor.info)
                continue

        data = get_story_data(url)
        ctx.obj["track-data"][story_id] = data

        save_to_track_file(ctx.obj["track-data"])

        click.secho(
            f'"{data["title"]}" ({story_id}) has been added to the tracked list.',
            fg=EchoColor.success,
        )

        if not skip_download:
            download_story(data)

        click.echo()


@main.command(short_help="Untracks stories.")
@click.argument("story-ids", nargs=-1)
@click.pass_context
def untrack(ctx, story_ids):
    """Removes the stories of the given STORY_ID from the tracking list if they
    exist."""
    for story_id in story_ids:
        if story_id not in ctx.obj["track-data"]:
            click.secho(
                f"There is no story of ID {story_id} on the tracked list.",
                fg=EchoColor.error,
            )
            continue

        title = ctx.obj["track-data"][story_id]["title"]
        del ctx.obj["track-data"][story_id]

        save_to_track_file(ctx.obj["track-data"])

        click.secho(
            f'Successfully removed "{title}" ({story_id}) from the tracked list.',
            fg=EchoColor.success,
        )


@main.command("list")
@click.pass_context
def _list(ctx):
    """List all tracked stories."""
    if not ctx.obj["track-data"]:
        click.secho("There are no tracked stories.", fg=EchoColor.error)
        return

    def echo_value(items):
        k = click.style(items[0], fg="bright_white")
        v = get_highlighted_value(items[1])
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
                VALUE_TO_STATUS_NAME.get(tracker_data["completion-status"]),
            ]
        )
        click.echo()


@main.command()
@click.option(
    "--force", is_flag=True, help="Force download all tracked stories.",
)
@click.pass_context
def download(ctx, force):
    """Download all tracked stories that have updated.

    If a story is registered as 'Completed', you will be asked if you still
    want to check for an update on it."""
    if not ctx.obj["track-data"]:
        click.secho("There are no tracked stories.", fg=EchoColor.error)
        return

    for story_id, tracker_data in ctx.obj["track-data"].items():
        title = tracker_data["title"]
        if not force:
            if not tracker_data["completion-status"] == StoryStatus.incomplete.value:
                status_name = VALUE_TO_STATUS_NAME.get(
                    tracker_data["completion-status"]
                )

                msg = click.style(
                    f'"{title}" ({story_id}) has been marked as "{status_name}" '
                    "by the author. Do you want to still check for an update on it?",
                    fg=EchoColor.confirm_prompt,
                )
                if not click.confirm(msg):
                    click.secho(
                        "Skipping story.", fg=EchoColor.info,
                    )
                    click.echo()
                    continue

            click.secho(
                f'Checking if "{title}" ({story_id}) had an update...',
                fg=EchoColor.info,
            )

        page_data = get_story_data(tracker_data["url"], do_echoes=force)
        # Saving the obtained data now to at least ensure saving completion
        # status changes. The request is already made anyway, so why not.
        ctx.obj["track-data"][story_id] = page_data

        if not has_an_update(page_data, tracker_data):
            click.secho("Story didn't have an update.", fg="bright_yellow")

            if force:
                click.secho("Force downloading story.", fg="bright_yellow")
            elif not force:
                click.echo()
                continue

        download_story(page_data)
        click.echo()

        sleep(DOWNLOAD_DELAY)

    save_to_track_file(ctx.obj["track-data"])


if __name__ == "__main__":
    main(obj={})
