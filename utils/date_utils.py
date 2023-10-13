from datetime import datetime, timedelta


def add_hours_to_date(iso8601_date: str, hour_offset=2):
    try:
        # Parse the ISO 8601 date string into a datetime object
        input_datetime = datetime.fromisoformat(iso8601_date)

        # Add the specified number of hours
        result_datetime = input_datetime + timedelta(hours=hour_offset)

        # Convert the result back to ISO 8601 format
        result_iso8601 = result_datetime.isoformat()

        return result_iso8601
    except ValueError:
        return None  # Handle invalid input gracefully
