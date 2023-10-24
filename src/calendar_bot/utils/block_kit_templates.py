import json


def confirm_message_block_kit(channel_id, message_ts, user_id):
    return {
        "blocks": [
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "It looks like you are requesting support.  Would you like to run an automated diagnostics report to assist our volunteers?",
                    }
                ],
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "emoji": True, "text": "Run report"},
                        "style": "primary",
                        "value": json.dumps({"channel": channel_id, "ts": message_ts, "user": user_id}),
                        "action_id": "run_suggestion_button_ok",
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "emoji": True, "text": "No thanks"},
                        "action_id": "run_suggestion_button_no",
                    },
                ],
            },
        ]
    }


def edit_dialog_block_kit(channel_id, message_ts, user_id, nn=None):
    return {
        "type": "modal",
        "callback_id": "run_suggestion_submit_ok",
        "private_metadata": json.dumps({"channel": channel_id, "ts": message_ts, "user": user_id}),
        "title": {"type": "plain_text", "text": "Run node diagnostics", "emoji": True},
        "submit": {"type": "plain_text", "text": "Submit", "emoji": True},
        "close": {"type": "plain_text", "text": "Cancel", "emoji": True},
        "blocks": [
            {
                "type": "input",
                "optional": True,
                "block_id": "numberInputBlock",
                "element": get_default_nn_element_field(nn),
                "label": {"type": "plain_text", "text": "Node Number or Install Number:", "emoji": True},
            },
        ],
    }
