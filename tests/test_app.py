import os

from dotenv import load_dotenv

from event_extractor import get_event_data
from google_calendar import CalendarClient
from query import get_event_messages
from utils.date_utils import add_hours_to_date

load_dotenv()

calendar_client = CalendarClient(os.environ.get("TEST_CALENDAR_ID"))


def print_event_data():
    messages = get_event_messages()
    event_data = get_event_data(messages[0]["ts"], messages[0]["text"])
    print(event_data)


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


def create_multiple_events(message_count=10):
    messages = get_event_messages(message_count=message_count)
    # calendar_client = CalendarClient()

    for message in messages:
        try:
            create_event(message)
        except Exception as e:
            print(e)
            print("Error creating event")
            continue


if __name__ == "__main__":
    # create_event()
    create_multiple_events(message_count=10)
