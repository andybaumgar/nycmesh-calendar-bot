import datetime
import json
import os
from dataclasses import asdict, dataclass
from typing import Dict, TypedDict

import openai
from dotenv import load_dotenv

load_dotenv()

# Set your OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]


def unix_time_to_date(unix_time: str) -> str:
    return datetime.datetime.fromtimestamp(int(float(unix_time))).strftime("%Y-%m-%d")


@dataclass
class EventData:
    date: str
    title: str
    is_event: bool


def get_calendar_prompt(date_ts: str, message: str) -> str:
    date = unix_time_to_date(date_ts)

    prompt = f"""Given that today is {date}, what is the date mentioned in this message below?  Also include a title (try your best if one is not available).  Also include a is_event field which contains a boolean which corresponds to wheather the input messages appears to be a event opportunity.  Messages which appear to be responses or questions should return false.  These responses will not mention words like "opportunity" and be spoken in a less professional voice.  Messages that are empty should return false.  Please respond with the following json format {{"date":[yyy-mm-ddThh:mm:ss], "title":[title], "is_event":[is_event_boolean]}}.  Do not include any other text. "{message}" """

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
    prompt = get_calendar_prompt(date_ts, message)
    response = execute_prompt(prompt)
    data = json.loads(response["content"])
    event_data = EventData(**data)

    return event_data


if __name__ == "__main__":
    # Send a message to ChatGPT 3.5
    message = "Hello, ChatGPT!"
    response = execute_prompt(message)

    # Print the response
    print(response)
