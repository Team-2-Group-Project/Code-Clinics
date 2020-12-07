from __future__ import print_function
import pickle
import os.path
import sys, datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json
from datetime import timedelta


def creating_service():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '.credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('calendar', 'v3', credentials=creds)
    return service


def fb(date, time):
    """
    Needs to be in the ISO FORMAT for it to work properly...
    """
    service = creating_service()
    event = {
        "timeMin": (make_datetime_from_string(f'{date}T{time}:00+0200')).isoformat(),
        "timeMax": (make_datetime_from_string(f'{date}T{time}:00+0200')+timedelta(minutes = 90)).isoformat(),
        "timeZone": 'Africa/Johannesburg',
        "items": [
            {
                "id": 'msegal@student.wethinkcode.co.za'
            },
            {
                'id': 'teamtwotesting@gmail.com'
            }
        ]
    }

    eventsResult = service.freebusy().query(body=event).execute()
    return eventsResult


def make_datetime_from_string(string):
    """
    Creates a dattime object form a given string
    Parameter:  string (yyy-mm-ddTHH:MM:00+0200)
    Returns:    datetime object
    """
    return datetime.datetime.strptime(string, "%Y-%m-%dT%H:%M:%S%z")


def validate_douplicate_slots():
    events = fb('2020-12-11', '10:00')
    two_cals = events['calendars']
    patient, clinic = two_cals['msegal@student.wethinkcode.co.za'], two_cals['teamtwotesting@gmail.com']

    print("patient: ",patient)
    print("clinic: ", clinic)

    if patient['busy'] == [] and clinic['busy'] == []:
        print("both slots are empty")
    else:
        print("someone has something on")


    return

validate_douplicate_slots()
# print(fb('2020-12-11', '10:00'))
