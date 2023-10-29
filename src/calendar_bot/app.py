import json
import os
from functools import partial

import requests
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from .event_extractor import EventData, get_event_data, get_event_data_summary
from .google_calendar import GoogleCalendarClient
from .query_slack import SlackMessage, get_username
from .utils.block_kit_templates import confirm_message_block_kit
from .utils.message_classification import is_in_volunteer_channel
from .utils.post_event import post_calendar_event_from_event

load_dotenv()

google_calendar_client = GoogleCalendarClient(calendar_id=os.environ.get("CALENDAR_ID"))


def run_app(config):
    print("Starting bolt app...")

    app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

    @app.event(
        event={"type": "message", "subtype": None},
        # matchers=[
        #     partial(is_in_volunteer_channel, support_channel_ids=config["channel_ids"]),
        # ],
    )
    def respond_with_calendar_suggestion(message):
        print("test")
        event_data = get_event_data(message["ts"], message["text"])
        summary = get_event_data_summary(event_data)
        link = app.client.chat_getPermalink(message_ts=message["ts"], channel=message["channel"]).data["permalink"]

        app.client.chat_postEphemeral(
            channel=message["channel"],
            blocks=confirm_message_block_kit(
                channel_id=message["channel"],
                message_ts=message["ts"],
                user_id=message["user"],
                summary=summary,
                link=link,
                event_data=event_data,
                original_text=message["text"],
            )["blocks"],
            text="New volunteer message detected, offering to add event to calendar on supported platforms",
            user=message["user"],
            metadata="test",
        )

    @app.action("calendar_suggestion_ok")
    def calendar_suggestion_ok(ack, body, logger):
        ack()

        metadata = json.loads(body["actions"][0]["value"])
        event_data = EventData.from_json(metadata["event_data"])
        username = get_username(metadata["user_id"], app.client)
        message_data = SlackMessage(
            ts=metadata["ts"], text=metadata["original_text"], permalink=metadata["link"], username=username
        )
        message_data.link = metadata["link"]
        post_calendar_event_from_event(
            event_data=event_data,
            calendar_client=google_calendar_client,
            hour_offset=2,
            slack_message=message_data,
        )

        requests.post(
            body["response_url"],
            json={"response_type": "ephemeral", "text": "", "replace_original": True, "delete_original": True},
        )

        # TODO add calendar link to thread

    #     requests.post(
    #         body["response_url"],
    #         json={"response_type": "ephemeral", "text": "", "replace_original": True, "delete_original": True},
    #     )

    # @app.action("calendar_suggestion_edit")
    # def calendar_suggestion_edit(ack, body, logger):
    #     ack()

    #     metadata = json.loads(body["actions"][0]["value"])
    #     user = MeshUser(app, metadata["user"], config["nn_property_id"], database_client_cached=database_client_cached)
    #     nn = user.network_number

    #     app.client.views_open(
    #         trigger_id=body["trigger_id"],
    #         view=help_suggestion_dialog_block_kit(metadata["channel"], metadata["ts"], metadata["user"], nn=nn),
    #     )

    #     requests.post(
    #         body["response_url"],
    #         json={"response_type": "ephemeral", "text": "", "replace_original": True, "delete_original": True},
    #     )

    @app.action("calendar_suggestion_no")
    def calendar_suggestion_no(ack, body, logger):
        ack()

        requests.post(
            body["response_url"],
            json={"response_type": "ephemeral", "text": "", "replace_original": True, "delete_original": True},
        )

    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()
