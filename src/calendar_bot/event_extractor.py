import json
import os
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Dict, TypedDict

import openai
from dataclasses_json import dataclass_json
from dotenv import load_dotenv

from . import config

load_dotenv()

# Set your OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]


def unix_time_to_date(unix_time: str) -> str:
    return datetime.fromtimestamp(int(float(unix_time))).strftime("%Y-%m-%d")


@dataclass_json
@dataclass
class EventData:
    date: datetime
    title: str
    is_event: bool
    description: str


def get_calendar_prompt(date_ts: str, message: str) -> str:
    date = unix_time_to_date(date_ts)

    prompt = config.prompt.format(date=date, message=message)

    return prompt


# Define a function to send a message to ChatGPT 3.5
def execute_prompt(prompt: str) -> str:
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )

    return completion.choices[0].message


def get_event_data(date_ts: str, message: str) -> EventData:
    if message == "":
        return EventData(date=None, title=None, is_event=False, description="")
    prompt = get_calendar_prompt(date_ts, message)
    response = execute_prompt(prompt)
    data = json.loads(response["content"])
    if data["date"] is not None:
        date_object = datetime.strptime(data["date"], "%Y-%m-%dT%H:%M:%S")
        data["date"] = date_object
    event_data = EventData(**data, description=message)

    return event_data


def get_event_data_summary(event_data: EventData) -> str:
    human_readable_date = event_data.date.strftime("%A, %B %d, %Y %I:%M %p")
    summary = (
        f"""*Title:* {event_data.title}\n*Date:* {human_readable_date} \n*Description:* {event_data.description}"""
    )

    return summary


if __name__ == "__main__":
    # Send a message to ChatGPT 3.5
    message = "Hello, ChatGPT!"
    response = execute_prompt(message)

    # Print the response
    print(response)
