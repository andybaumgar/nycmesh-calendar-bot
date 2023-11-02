from datetime import datetime, timedelta


def add_hours_to_date(iso8601_date: str, hour_offset=2):
    try:
        input_datetime = datetime.fromisoformat(iso8601_date)
        result_datetime = input_datetime + timedelta(hours=hour_offset)
        result_iso8601 = result_datetime.isoformat()

        return result_iso8601
    except ValueError:
        return None
