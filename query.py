import os

from dotenv import load_dotenv
from slack_bolt import App

load_dotenv()


def get_event_messages():
    app = App(token=os.environ["SLACK_USER_TOKEN"], name="Query Bot")

    query = "in:#volunteer -threads:replies"
    search_result = app.client.search_messages(query=query, sort="timestamp", count=100)

    messages = search_result._initial_data["messages"]["matches"]

    return messages


if __name__ == "__main__":
    get_event_messages()
