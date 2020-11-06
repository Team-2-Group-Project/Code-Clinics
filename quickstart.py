from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import json
import deletion.delete as delete
import insertion.insert as insert
import update.update as update

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def main():
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
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service


def create_calendar_events(service, future_date):
    """
    Creates the calendar based on the days that will need to show up for the given days
    """
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    a_week = datetime.date.today() + datetime.timedelta(days=future_date)
    a_week = str(a_week) + 'T23:59:59.999999+02:00'

    print(f'Getting the upcoming {a_week} days calendar')

    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          timeMax=a_week, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    with open('.calendar.json', 'w+') as f:
        json.dump(events, f)

    return events


def meetings_lists(events):
    which_meeting = input("meeting name?: ")
    meetings = [item for item in events if item["summary"] == which_meeting]

    if not meetings:
        print('No upcoming meetings found.')
    for meet in meetings:
        start = meet['start'].get('dateTime', meet['start'].get('date'))
        print(start, meet['summary'])

    calander_id = str()

    if len(meetings) > 1:
        meetin_time = input("which meeting time would you like to choose? ")
        calander_id = meetings[int(meetin_time)-1]['id']
    elif len(meetings) == 1:
        calander_id = meetings[0]['id']
    else:
        print("There are no meetings")
        return service, ''
    
    return calander_id


if __name__ == '__main__':
    service = main()
    events = create_calendar_events(service, 7)
    calander_id = meetings_lists(events)

    # insert.insert_event(service)
    # update.update_event(service, calander_id)
    # delete.delete_event(service, calander_id)
