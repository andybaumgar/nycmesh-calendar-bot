from converter import get_event_data
from google_calendar import CalendarClient
from query import get_event_messages

import os

from dotenv import load_dotenv

from event_extractor import get_event_data
from google_calendar import CalendarClient
from query import get_event_messages
from utils.date_utils import add_hours_to_date

load_dotenv()

calendar_client = CalendarClient(os.environ.get("TEST_CALENDAR_ID"))

def create_event(message):
    event_data = get_event_data(message["ts"], message["text"])

    link = message["permalink"]
    username = message["username"]
    message_text = message["text"]
    description = f"""IMPORTANT: This event is auto generated.  Please confirm event details in Slack: {link}\nEvent poster: {username}\nEvent description: {message_text}"""

    print(event_data)
    end_with_offset = add_hours_to_date(event_data["date"], 2)
    calendar_client.create_event(
        summary=event_data["title"],
        description=description,
        start=event_data["date"],
        end=end_with_offset,
    )

if __name__ == "__main__":
    # create_multiple_events()
    # print_event_data()
