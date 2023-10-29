from calendar_bot.query_slack import SlackMessage

from .. import config


def add_description_disclaimer(message: SlackMessage):
    m = message
    description = config.description_disclaimer.format(link=m.link, username=m.username, message_text=m.text)

    return description
