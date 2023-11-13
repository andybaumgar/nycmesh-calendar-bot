import click

from calendar_bot import app
from calendar_bot.constants import DEFAULT_CHANNEL_IDS


@click.command()
@click.option(
    "--channel-ids",
    default=DEFAULT_CHANNEL_IDS,
    help="The Slack ID number for the channel to run the bot in",
    multiple=True,
)
def main(channel_ids):
    app.run_app({"channel_ids": channel_ids})


if __name__ == "__main__":
    main()
