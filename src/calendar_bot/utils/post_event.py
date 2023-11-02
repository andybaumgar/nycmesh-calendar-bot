from ..event_extractor import EventData, get_event_data
from ..google_calendar import GoogleCalendarClient
from ..slack import SlackMessage
from .date_utils import add_hours_to_date
from .format_event_description import add_description_disclaimer


def post_calendar_event_link_to_slack(app=None, channel_id=None, calendar_link=None, thread_ts=None):
    text = f"Calendar event created: <{calendar_link}|link>"

    app.client.chat_postMessage(channel=channel_id, thread_ts=thread_ts, text=text, unfurl_links=False)


def post_calendar_event_from_event(
    event_data: EventData = None,
    calendar_client: GoogleCalendarClient = None,
    hour_offset: float = 0,
    slack_message: SlackMessage = None,
    app=None,
):
    description = add_description_disclaimer(slack_message.link)

    end_with_offset = add_hours_to_date(event_data.date.isoformat(), hour_offset=hour_offset)

    event = calendar_client.create_event(
        summary=event_data.title,
        description=description,
        start=event_data.date.isoformat(),
        end=end_with_offset,
    )

    if app is None:
        return event

    post_calendar_event_link_to_slack(
        app=app, channel_id=slack_message.channel_id, calendar_link=event["htmlLink"], thread_ts=slack_message.ts
    )

    return event
