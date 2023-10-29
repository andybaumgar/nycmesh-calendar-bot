import os

from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv()


class GoogleCalendarClient:
    def __init__(self, calendar_id=None):
        self.calendar_id = calendar_id

        SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
        # created in Google Cloud admin
        SERVICE_ACCOUNT_FILE = "credentials.json"

        credentials_dict = self._get_sheets_credentials_from_env()
        credentials = service_account.Credentials.from_service_account_info(credentials_dict)
        self.service = build("calendar", "v3", credentials=credentials)

    def _get_sheets_credentials_from_env(self):
        try:
            credentials_mapping = {
                "type": "GOOGLE_SHEETS_TYPE",
                "project_id": "GOOGLE_SHEETS_PROJECT_ID",
                "private_key_id": "GOOGLE_SHEETS_PRIVATE_KEY_ID",
                "private_key": "GOOGLE_SHEETS_PRIVATE_KEY",
                "client_email": "GOOGLE_SHEETS_CLIEND_EMAIL",
                "client_id": "GOOGLE_SHEETS_CLIENT_ID",
                "auth_uri": "GOOGLE_SHEETS_AUTH_URI",
                "token_uri": "GOOGLE_SHEETS_TOKEN_URI",
                "auth_provider_x509_cert_url": "GOOGLE_SHEETS_AUTH_PROVIDER_X509_CERT_URL",
                "client_x509_cert_url": "GOOGLE_SHEETS_CLIENT_509_CERT_URL",
            }

            credentials = {}
            for key, value in credentials_mapping.items():
                credentials[key] = os.environ.get(value)

            credentials["private_key"] = credentials["private_key"].replace("\\n", "\n")

            return credentials
        except Exception as e:
            print(e)
            raise ValueError("Problem parsing Google Sheets credentials")

    def create_event(self, summary: str, description: str, start: str, end: str):
        # Define the event details
        event = {
            "summary": summary,
            "description": description,
            "start": {
                "dateTime": start,
                "timeZone": "America/New_York",
            },
            "end": {"dateTime": end, "timeZone": "America/New_York"},
        }

        event = (
            self.service.events()
            .insert(
                calendarId=self.calendar_id,
                body=event,
            )
            .execute()
        )


if __name__ == "__main__":
    calendar_client = GoogleCalendarClient(os.environ.get("TEST_CALENDAR_ID"))
    # calendar_client.create_event(summary, description, start, end)
