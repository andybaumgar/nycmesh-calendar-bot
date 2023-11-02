def is_in_volunteer_channel(message, support_channel_ids):
    return message["channel"] in support_channel_ids
