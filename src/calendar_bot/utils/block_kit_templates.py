import json

from calendar_bot.event_extractor import EventData

from ..slack import SlackMessage


def confirm_message_block_kit(
    message: SlackMessage,
    event_data: EventData = None,
    summary: str = None,
):
    return {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"It looks like you are posting a volunteer opportunity.\nWould you like to add the event to our calendar?\n\nDetails:\n\n{summary}",
                },
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "emoji": True, "text": "Post event"},
                        "style": "primary",
                        "value": json.dumps(
                            {
                                "message": message.to_json(),
                                "event_data": event_data.to_json(),
                            }
                        ),
                        "action_id": "calendar_suggestion_ok",
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "emoji": True, "text": "Edit"},
                        "action_id": "calendar_suggestion_edit",
                        "value": json.dumps(
                            {
                                "message": message.to_json(),
                                "event_data": event_data.to_json(),
                            }
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


def edit_dialog_block_kit(
    message: SlackMessage,
    event_data: EventData = None,
):
    return {
        "type": "modal",
        "callback_id": "calendar_edit_dialog_submit",
        "private_metadata": json.dumps(
            {
                "message": message.to_json(),
                "event_data": event_data.to_json(),
            }
        ),
        "title": {"type": "plain_text", "text": "Edit calendar post", "emoji": True},
        "submit": {"type": "plain_text", "text": "Post event ", "emoji": True},
        "close": {"type": "plain_text", "text": "Cancel", "emoji": True},
        "blocks": [
            {
                "type": "input",
                "block_id": "edit_date",
                "element": {
                    "type": "datetimepicker",
                    "action_id": "datetimepicker-action",
                    "initial_date_time": int(event_data.date.timestamp()),
                },
                "label": {"type": "plain_text", "text": "Event date", "emoji": True},
            },
            {
                "type": "input",
                "block_id": "edit_title",
                "label": {"type": "plain_text", "text": "Event title"},
                "element": {
                    "type": "plain_text_input",
                    "action_id": "plain_input",
                    "placeholder": {"type": "plain_text", "text": event_data.title},
                },
            },
        ],
    }
