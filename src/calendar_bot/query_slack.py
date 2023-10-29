import json
import os
from dataclasses import asdict, dataclass
from urllib.parse import quote, urlencode

from dotenv import load_dotenv
from slack_bolt import App

load_dotenv()


# create data class  returned slack messages
@dataclass
class SlackMessage:
    ts: str
    text: str
    permalink: str
    username: str
    link: str = None


def save_messages(messages: SlackMessage, file_path):
    with open(file_path, "w") as f:
        message_dict = [message.__dict__ for message in messages]
        message_json = json.dumps(message_dict, sort_keys=True, indent=4, separators=(",", ": "))

        f.write(str(message_json))
        f.write("\n")


def get_slack_event_messages(message_count=10):
    app = App(token=os.environ["SLACK_USER_TOKEN"], name="Query Bot")

    query = "in:#volunteer -threads:replies"
    search_result = app.client.search_messages(query=query, sort="timestamp", count=message_count)

    raw_messages = search_result._initial_data["messages"]["matches"]
    slack_messages = [SlackMessage(message) for message in raw_messages]

    return slack_messages


def get_username(id, slack_client):
    try:
        response = slack_client.users_info(user=id)
        if response["ok"]:
            user_info = response["user"]
            return user_info["real_name"]
        else:
            return None
    except Exception as e:
        return None


if __name__ == "__main__":
    get_slack_event_messages()
