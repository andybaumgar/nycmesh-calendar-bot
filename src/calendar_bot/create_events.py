import os

from dotenv import load_dotenv

from calendar_bot.event_extractor import get_event_data
from calendar_bot.google_calendar import GoogleCalendarClient
from calendar_bot.query_slack import SlackMessage
from calendar_bot.utils.date_utils import add_hours_to_date

load_dotenv()

calendar_client = GoogleCalendarClient(os.environ.get("TEST_CALENDAR_ID"))


def create_event(message: SlackMessage):
    event_data = get_event_data(message.ts, message.text)

    m = message
    description = f"""IMPORTANT: This event is auto generated.  Please confirm event details in Slack: {m.link}\nEvent poster: {m.username}\nEvent description: {m.message_text}"""

    print(event_data)
    end_with_offset = add_hours_to_date(event_data["date"], 2)
    calendar_client.create_event(
        summary=event_data["title"],
        description=description,
        start=event_data["date"],
        end=end_with_offset,
    )


if __name__ == "__main__":
    pass
    # create_multiple_events()
    # print_event_data()
