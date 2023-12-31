import json
import os
import time
from datetime import datetime
from functools import partial

import pytz
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from .event_extractor import EventData, get_event_data, get_event_data_summary
from .google_calendar import GoogleCalendarClient
from .slack import SlackMessage, close_ephemeral, get_username
from .utils.block_kit_templates import confirm_message_block_kit, edit_dialog_block_kit
from .utils.message_classification import is_first_message_in_thread, is_in_target_channel
from .utils.post_event import post_calendar_event_from_event

load_dotenv()
google_calendar_client = GoogleCalendarClient(calendar_id=os.environ.get("CALENDAR_ID"))


def run_app(config):
    print("Starting bolt app...")

    app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

    @app.event(
        event={"type": "message", "subtype": None},
        matchers=[
            partial(is_in_target_channel, support_channel_ids=config["channel_ids"]),
            is_first_message_in_thread,
        ],
    )
    def respond_with_calendar_suggestion(message):
        link = app.client.chat_getPermalink(message_ts=message["ts"], channel=message["channel"]).data["permalink"]
        message_object = SlackMessage(
            ts=message["ts"],
            text=message["text"],
            username=get_username(message["user"], app.client),
            link=link,
            user_id=message["user"],
            channel_id=message["channel"],
        )

        event_data = get_event_data(message["ts"], message["text"])

        if not event_data.is_event:
            return

        summary = get_event_data_summary(event_data, link)

        app.client.chat_postEphemeral(
            channel=message["channel"],
            blocks=confirm_message_block_kit(
                message=message_object,
                summary=summary,
                event_data=event_data,
            )["blocks"],
            text="New volunteer message detected, offering to add event to calendar on supported platforms",
            user=message["user"],
            metadata="test",
        )

    def parse_metadata(body) -> (EventData, SlackMessage):
        metadata = json.loads(body["actions"][0]["value"])
        event = EventData.from_json(metadata["event_data"])
        message = SlackMessage.from_json(metadata["message"])

        return (event, message)

    @app.action("calendar_suggestion_ok")
    def calendar_suggestion_ok(ack, body, logger):
        ack()

        event, message = parse_metadata(body)

        post_calendar_event_from_event(
            event_data=event,
            calendar_client=google_calendar_client,
            hour_offset=2,
            slack_message=message,
            app=app,
        )

        close_ephemeral(body)

        # TODO add calendar link to thread

    @app.action("calendar_suggestion_edit")
    def calendar_suggestion_edit(ack, body, logger):
        ack()

        event, message = parse_metadata(body)

        app.client.views_open(
            trigger_id=body["trigger_id"],
            view=edit_dialog_block_kit(
                message=message,
                event_data=event,
            ),
        )

        close_ephemeral(body)

    @app.shortcut("manually_add_event")
    def manually_add_event(ack, shortcut, client):
        ack()

        link = app.client.chat_getPermalink(message_ts=shortcut["message_ts"], channel=shortcut["channel"]["id"]).data[
            "permalink"
        ]

        message = SlackMessage(
            ts=shortcut["message_ts"],
            text=shortcut["message"]["text"],
            username=get_username(shortcut["user"]["id"], app.client),
            link=link,
            user_id=shortcut["user"]["id"],
            channel_id=shortcut["channel"]["id"],
        )

        event = get_event_data(shortcut["message_ts"], shortcut["message"]["text"])

        summary = get_event_data_summary(event, link)

        app.client.chat_postEphemeral(
            channel=shortcut["channel"]["id"],
            blocks=confirm_message_block_kit(
                message=message,
                summary=summary,
                event_data=event,
            )["blocks"],
            text="New volunteer message detected, offering to add event to calendar on supported platforms",
            user=shortcut["user"]["id"],
            metadata="test",
        )

    @app.action("calendar_suggestion_no")
    def calendar_suggestion_no(ack, body, logger):
        ack()

        close_ephemeral(body)

    @app.view("calendar_edit_dialog_submit")
    def calendar_edit_dialog_submit(ack, body, client, view, logger):
        ack()

        metadata = json.loads(view["private_metadata"])
        event = EventData.from_json(metadata["event_data"])
        message = SlackMessage.from_json(metadata["message"])

        user_title = view["state"]["values"]["edit_title"]["plain_input"]["value"]

        # convert local timestamp into utc datetime
        user_ts = view["state"]["values"]["edit_date"]["datetimepicker-action"]["selected_date_time"]
        date_naive = datetime.fromtimestamp(user_ts)
        date_local = date_naive.astimezone()
        date_utc = date_local.astimezone(pytz.utc)

        event.date = date_utc
        event.title = user_title

        post_calendar_event_from_event(
            event_data=event,
            calendar_client=google_calendar_client,
            hour_offset=2,
            slack_message=message,
            app=app,
        )

    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()
