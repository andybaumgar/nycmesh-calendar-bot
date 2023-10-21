import os

from dotenv import load_dotenv

from event_extractor import get_event_data
from google_calendar import GoogleCalendarClient
from query_slack import SlackMessage

load_dotenv()

calendar_client = GoogleCalendarClient(os.environ.get("TEST_CALENDAR_ID"))


def test_good_message_coney_island():
    message = {
        "permalink": "https://nycmesh.slack.com/archives/CLMSV5KNG/p1696029394677579?thread_ts=1696029394.677579",
        "text": "Posting to volunteer again for the new people who have joined. We have an upcoming outreach event at the Coney Island Maker Faire on Oct 7th and 8th.\nLooking for people to help out with running the table.\n\nDetails: <https://nycmesh.slack.com/archives/C02UK9Z8W/p1693536918586919>",
        "ts": "1696029394.677579",
        "username": "lydon",
    }

    slack_message = SlackMessage(**message)
    event_data = get_event_data(slack_message.ts, slack_message.text)
    assert event_data.is_event == True


def test_good_message_with_link():
    message = {
        "permalink": "https://nycmesh.slack.com/archives/CLMSV5KNG/p1696029394677579?thread_ts=1696029394.677579",
        "text": "Posting to volunteer again for the new people who have joined. We have an upcoming outreach event at the Coney Island Maker Faire on Oct 7th and 8th.\nLooking for people to help out with running the table.\n\nDetails: <https://nycmesh.slack.com/archives/C02UK9Z8W/p1693536918586919>",
        "ts": "1696029394.677579",
        "username": "lydon",
    }

    slack_message = SlackMessage(**message)
    event_data = get_event_data(slack_message.ts, slack_message.text)
    assert event_data.is_event == True


def test_bad_random_message():
    message = {
        "permalink": "https://nycmesh.slack.com/archives/CLMSV5KNG/p1695770544800329",
        "text": "Im not too far away\u2014let me know what time",
        "ts": "1695770544.800329",
        "username": "karl.wenninger",
    }

    slack_message = SlackMessage(**message)
    event_data = get_event_data(slack_message.ts, slack_message.text)
    assert event_data.is_event == False, f"Message {message} should not be an event"


def test_bad_empty_message():
    message = {
        "permalink": "https://nycmesh.slack.com/archives/CLMSV5KNG/p1692985043276939",
        "text": "",
        "ts": "1692985043.276939",
        "username": "create volunteer opportunity",
    }

    slack_message = SlackMessage(**message)
    event_data = get_event_data(slack_message.ts, slack_message.text)
    assert event_data.is_event == False, f"Message {message} should not be an event"


if __name__ == "__main__":
    pass