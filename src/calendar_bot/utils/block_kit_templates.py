import json


def confirm_message_block_kit(channel_id=None, message_ts=None, user_id=None, calendar_text=None):
    return {
        "blocks": [
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"It looks like you are posting a volunteer opportunity.  Would you like to post the event to our calendar?\n\nParsed event details:\n\n{calendar_text}",
                    }
                ],
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "emoji": True, "text": "Post event"},
                        "style": "primary",
                        "value": json.dumps(
                            {"channel": channel_id, "ts": message_ts, "user": user_id, calendar_text: calendar_text}
                        ),
                        "action_id": "calendar_suggestion_ok",
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "emoji": True, "text": "Edit"},
                        "action_id": "calendar_suggestion_edit",
                        "value": json.dumps(
                            {"channel": channel_id, "ts": message_ts, "user": user_id, "calendar_text": calendar_text}
                        ),
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "emoji": True, "text": "Cancel"},
                        "action_id": "calendar_suggestion_no",
                    },
                ],
            },
        ]
    }


def edit_dialog_block_kit(channel_id, message_ts, user_id, calendar_text):
    return {
        "type": "modal",
        "callback_id": "calendar_edit_dialog_submit",
        "private_metadata": json.dumps(
            {"channel": channel_id, "ts": message_ts, "user": user_id, "calendar_text": calendar_text}
        ),
        "title": {"type": "plain_text", "text": "Run node diagnostics", "emoji": True},
        "submit": {"type": "plain_text", "text": "Submit", "emoji": True},
        "close": {"type": "plain_text", "text": "Cancel", "emoji": True},
        "blocks": [
            {
                "type": "input",
                "optional": True,
                "block_id": "numberInputBlock",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "plain_input",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Type your edits here, ex. 'date should be the 12th'",
                    },
                },
                "label": {"type": "plain_text", "text": "Node Number or Install Number:", "emoji": True},
            },
        ],
    }
