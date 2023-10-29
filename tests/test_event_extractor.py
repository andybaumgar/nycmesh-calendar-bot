import os
from datetime import datetime

from dotenv import load_dotenv

from calendar_bot.event_extractor import EventData, get_event_data, get_event_data_summary
from calendar_bot.google_calendar import GoogleCalendarClient
from calendar_bot.slack import SlackMessage

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
    print(event_data)
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


def test_day_of_week_daniel():
    message = {
        "permalink": "https://nycmesh.slack.com/archives/CLMSV5KNG/p1696029394677579?thread_ts=1696029394.677579",
        "text": "Good evening, I am planning for Sunday (possible start time 10AM) to cut back over to newly ran ground fiber, and I could use some help with some fiber splicing, installing new enclosures, and switching back over with minimal downtime. Would anyone be available?",
        "ts": "1698548742.677579",
        "username": "daniel",
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


def test_get_event_data_summary():
    date_object = datetime.strptime("2021-09-23T00:00:00", "%Y-%m-%dT%H:%M:%S")

    event_data = EventData(
        date=date_object,
        title="Test event title",
        is_event=True,
        description="Test event description",
    )

    summary = get_event_data_summary(event_data)

    print(summary)


def test_to_json():
    date_object = datetime.strptime("2021-09-23T00:00:00", "%Y-%m-%dT%H:%M:%S")
    event_data = EventData(
        date=date_object,
        title="Test event title",
        is_event=True,
        description="Test event description",
    )
    json_data = event_data.to_json()
    print(json_data)

    # assert summary == expected_summary, f"Summary {summary} does not match expected summary {expected_summary}"
