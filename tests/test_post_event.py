import os
from datetime import datetime

from dotenv import load_dotenv

from calendar_bot.event_extractor import EventData
from calendar_bot.google_calendar import GoogleCalendarClient
from calendar_bot.utils.post_event import post_calendar_event_from_event

load_dotenv()

google_calendar_client = GoogleCalendarClient(calendar_id=os.environ.get("TEST_CALENDAR_ID"))


def test_post_calendar_event_from_event():
    date_object = datetime.strptime("2021-09-23T00:00:00", "%Y-%m-%dT%H:%M:%S")
    event_data = EventData(
        date=date_object,
        title="test_post_calendar_event_from_event",
        is_event=True,
        description="Test event description",
    )

    post_calendar_event_from_event(event_data=event_data, calendar_client=google_calendar_client, hour_offset=2)
