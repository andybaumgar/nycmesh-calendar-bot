from ..event_extractor import EventData, get_event_data
from ..google_calendar import GoogleCalendarClient
from ..query_slack import SlackMessage
from .date_utils import add_hours_to_date
from .format_event_description import add_description_disclaimer


def post_calendar_event_from_event(
    event_data: EventData = None,
    calendar_client: GoogleCalendarClient = None,
    hour_offset: float = 0,
    slack_message: SlackMessage = None,
):
    """slack_message is optional and used to add description disclaimer"""

    if slack_message is not None:
        description = add_description_disclaimer(slack_message)
    else:
        description = event_data.description

    end_with_offset = add_hours_to_date(event_data.date.isoformat(), hour_offset=hour_offset)
    calendar_client.create_event(
        summary=event_data.title,
        description=description,
        start=event_data.date.isoformat(),
        end=end_with_offset,
    )
