import os
from functools import partial

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from calendar_bot.utils.block_kit_templates import confirm_message_block_kit
from calendar_bot.utils.message_classification import is_in_volunteer_channel

load_dotenv()


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
        root_message_ts = message["thread_ts"] if "thread_ts" in message else message["ts"]
        app.client.chat_postEphemeral(
            channel=message["channel"],
            blocks=confirm_message_block_kit(
                channel_id=message["channel"],
                message_ts=root_message_ts,
                user_id=message["user"],
                calendar_text="Test message text",
            )["blocks"],
            text="New volunteer message detected, offering to add event to calendar on supported platforms",
            user=message["user"],
            metadata="test",
        )

    # @app.action("calendar_suggestion_ok")
    # def calendar_suggestion_ok(ack, body, logger):
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

    # @app.action("calendar_suggestion_no")
    # def calendar_suggestion_no(ack, body, logger):
    #     ack()

    #     requests.post(
    #         body["response_url"],
    #         json={"response_type": "ephemeral", "text": "", "replace_original": True, "delete_original": True},
    #     )

    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()
