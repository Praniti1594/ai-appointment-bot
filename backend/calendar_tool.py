import os
import datetime
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

# ✅ Load environment variables
load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")  # ✅ Loaded from .env
CALENDAR_ID = os.getenv("CALENDAR_ID")                    # ✅ Loaded from .env

# ✅ Create credentials and service
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('calendar', 'v3', credentials=credentials)

# ✅ Check availability between start and end time
def check_availability(start_time, end_time):
    print(f"🔍 Checking availability from {start_time} to {end_time}")

    events = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=start_time.isoformat(),
        timeMax=end_time.isoformat(),
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    is_free = len(events.get('items', [])) == 0
    print(f"📅 Slot is {'available' if is_free else 'unavailable'}")
    return is_free

# ✅ Create calendar event
def create_event(summary, start_time, end_time):
    event = {
        'summary': summary,
        'start': {'dateTime': start_time.isoformat(), 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end_time.isoformat(), 'timeZone': 'Asia/Kolkata'},
    }
    created_event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return created_event['htmlLink']
