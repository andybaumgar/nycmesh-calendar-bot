from calendar_bot.slack import SlackMessage

from .. import config


def add_description_disclaimer(link):
    description = config.description_disclaimer.format(link=link)

    return description
