import os
import datetime as dt

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]

_HERE = os.path.dirname(__file__)
CREDENTIALS_FILE = os.path.join(_HERE, "credentials.json")
TOKEN_FILE = os.path.join(_HERE, "token.json")

DEFAULT_START_HOUR = 17


def get_calendar_service():
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                raise RuntimeError(
                    f"Missing {CREDENTIALS_FILE}. Download your OAuth client "
                    f"JSON from Google Cloud Console and save it there."
                )
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)


def _session_to_event(session):
    date = session["date"]
    hours = session.get("hours", 1)

    start = dt.datetime(date.year, date.month, date.day, DEFAULT_START_HOUR)
    end = start + dt.timedelta(hours=hours)

    return {
        "summary": f"Study: {session['task']}",
        "description": "Auto-scheduled by Studifly.",
        "start": {"dateTime": start.isoformat()},
        "end": {"dateTime": end.isoformat()},
    }


def add_event(session, service=None):
    if service is None:
        service = get_calendar_service()

    event = service.events().insert(
        calendarId="primary",
        body=_session_to_event(session),
    ).execute()

    return event.get("htmlLink")


def add_sessions(sessions):
    service = get_calendar_service()
    links = []
    for s in sessions:
        links.append(add_event(s, service=service))
    return links
