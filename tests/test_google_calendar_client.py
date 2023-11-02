import os
from datetime import datetime

from dotenv import load_dotenv

from calendar_bot.event_extractor import EventData
from calendar_bot.google_calendar import GoogleCalendarClient

load_dotenv()

google_calendar_client = GoogleCalendarClient(calendar_id=os.environ.get("TEST_CALENDAR_ID"))


def test_create_event():
    google_calendar_client.create_event(
        summary="test_create_event",
        description="Test event description",
        start="2021-09-23T00:00:00",
        end="2021-09-23T02:00:00",
    )
