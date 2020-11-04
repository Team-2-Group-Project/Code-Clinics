from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json

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

# Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print(now)
    # Optional change days=<var> and ask user howlong into the future they want to look
    a_week = datetime.date.today() + datetime.timedelta(days=7)
    a_week = str(a_week) + 'T23:59:59.999999+02:00'

    print(f'Getting the upcoming {a_week} days calendar')

    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          timeMax=a_week, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    with open('calendar.json', 'w+') as f:
        json.dump(events, f)

    meetings = [item for item in events if item["summary"] == 'bob']
    print(meetings)

    individual_time = []

    if len(meetings) > 1:
        meetin_time = input("which meeting time would you like to choose? ")
        individual_time = [
            item for item in meetings if item["start"]["dateTime"] == meetin_time]

    print(individual_time)
    print(individual_time[0]['id'])
    # event = {
    #     'summary': input("What would you like to call this meeting? "),
    #     'location': '',
    #     'description': input("Please tell us what you need help with? "),
    #     'start': {
    #         'dateTime': "2020-11-05T13:00:00-07:00",
    #         'timeZone': 'Africa/Johannesburg',
    #     },
    #     'end': {
    #         'dateTime': '2020-11-05T13:00:00-07:30',
    #         'timeZone': 'Africa/Johannesburg',
    #     },
    #     "hangoutLink": "https://meet.google.com/snz-hfvt-zuo?pli=1&authuser=0",
    #     # 'attendees': [
    #     #     {'email': 'bthompso@student.wethinkcode.co.za'},
    #     # ],
    #     'reminders': {
    #         'useDefault': False,
    #         'overrides': [
    #             {'method': 'email', 'minutes': 24 * 60},
    #             {'method': 'popup', 'minutes': 10},
    #         ],
    #     },
    #     'anyoneCanAddSelf': True,
    # }

    # event = service.events().insert(calendarId='primary', body=event).execute()

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

    service.events().delete(calendarId='primary',
                            eventId=individual_time[0]['id']).execute()


if __name__ == '__main__':
    main()
