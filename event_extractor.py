import datetime
import json
import os
from typing import Dict, TypedDict

import openai
from dotenv import load_dotenv

load_dotenv()

# Set your OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]


def unix_time_to_date(unix_time: str) -> str:
    return datetime.datetime.fromtimestamp(int(float(unix_time))).strftime("%Y-%m-%d")


def get_calendar_prompt(date_ts: str, message: str) -> str:
    date = unix_time_to_date(date_ts)

    prompt = f"""Given that today is {date}, what is the date mentioned in this message below?  Also include a title (try your best if one is not available).  Please respond with the following json format {{"date":[yyy-mm-ddThh:mm:ss], "title":[title]}}.  Do not include any other text. "{message}" """

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


class EventData(TypedDict):
    date: str
    title: str


def get_event_data(date_ts: str, message: str) -> EventData:
    prompt = get_calendar_prompt(date_ts, message)
    response = execute_prompt(prompt)
    data = json.loads(response["content"])
    if isinstance(data["date"], list):
        data["date"] = data["date"][0]

    return data


if __name__ == "__main__":
    # Send a message to ChatGPT 3.5
    message = "Hello, ChatGPT!"
    response = execute_prompt(message)

    # Print the response
    print(response)
