from converter import get_event_data
from query import get_event_messages

messages = get_event_messages()
event_data = get_event_data(messages[0]["ts"], messages[0]["text"])
print(event_data)
