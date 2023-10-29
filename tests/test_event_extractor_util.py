import os
from pathlib import Path

from calendar_bot.slack import get_slack_event_messages, save_messages


def update_saved_messages():
    messages = get_slack_event_messages()

    current_path = Path(__file__).parent.resolve()
    save_path = str(current_path / Path("data") / "messages.json")
    save_messages(messages, save_path)


if __name__ == "__main__":
    update_saved_messages()
