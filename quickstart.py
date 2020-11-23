from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json
import calendar_cc.calendar as p_calendar
import calendar_cc.client_calendar as c_calendar
import clinician
import patient
from clinician import insert as c_insert
from clinician import delete as c_delete
from clinician import update as c_update
from patient import insert as p_insert
# from patient import update as p_update
from patient import delete as p_delete
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']
valid_action = ["create", "update","meeting list","delete","exit","join"]


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
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('calendar', 'v3', credentials=creds)
    return service
print(("\033[1;32mWelcome to Code Clinic!\033[0m"))


def user_name():
    '''
    Asking for the username, therfore it can connect to their email address
    '''
    user_name = input((f"Enter your WeThinkCode Student User_Name: "))
    return user_name


def which_role(user_name):
    possible_roles = ['c','p','clinician', 'patient']
    role = input(f"Hello {user_name}, are you a Clinician (C) or a Patient (P)? ")
    while role.lower() not in possible_roles:
        role = input(f"Please state if you are a Clinician (C) or a Patient (P)? ")
    return role.lower()


def what_would():
    '''
    Storing the users response to the function it wants to perform
    '''
    if role == 'c' or role == 'clinician':
        help_doctor()
    else:
        help_patient()
    action = input(f"What would you like to do: ")
    if valid_command(action) == False:
        action = what_would()
    return action.lower()


def valid_command(action):
    if action in valid_action:
        return True
    else: 
        return False
    

def call_calendar(events, calendar):
    try:
        calendar.generate_table(8,events)
        calendar.table_data = []
    except:
        print("You have no meetings in your calendar")
    
def handle_command(action, service, user_name, role):
    '''
    Creating conditions that will take the users input
    , then performing the requested action
    '''
    calendar = c_calendar if role == "c" else p_calendar
    if action not in valid_action: 
        action = what_would()
    if role == 'c' or role == 'clinician':
        #print(help_doctor())
        if action == "create":
            events = create_calendar_events(service, 7)
            calendar.generate_table(8,events)
            c_insert.insert_event(service, user_name, calendar.table_data)
            calendar.table_data = []
        elif action == "update":
            events = create_calendar_events(service, 7)
            call_calendar(events, calendar)
            calander_id = meetings_lists(events)
            c_update.update_event(service, calander_id)
        elif action == "meeting list":
            events = create_calendar_events(service, 7)
            calendar.print_table(8, events)
            # meetings_lists(events)
        elif action == "delete":
            events = create_calendar_events(service, 7)
            call_calendar(events, calendar)
            calander_id = meetings_lists(events)
            c_delete.delete_event(service, calander_id)
        elif action == "exit":
            print("Thank you for using code clinic")
            return False
    if role == 'p' or role == 'patient':
        # print(help_patient())
        if action == "join":
            events = create_calendar_events(service, 7)
            call_calendar(events, calendar)
            calander_id = meetings_lists(events)
            p_insert.insert_patient(service, calander_id, user_name)
        elif action == "update":
            events = create_calendar_events(service, 7)
            call_calendar(events, calendar)
            calander_id = meetings_lists(events)
            # patient.update.update_event(service, calander_id)
        elif action == "meeting list":
            events = create_calendar_events(service, 7)
            call_calendar(events, calendar)
            # meetings_lists(events)
        elif action == "delete":
            events = create_calendar_events(service, 7)
            call_calendar(events, calendar)
            calander_id = meetings_lists(events)
            p_delete.delete_event(service, calander_id, user_name)
        elif action == "exit":
            print("Thank you for using code clinic")
            return False
    return True


def create_calendar_events(service, future_date):
    """
    Creates the calendar based on the days that will need to show up for the given days
    """
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    a_week = datetime.date.today() + datetime.timedelta(days=future_date)
    a_week = str(a_week) + 'T23:59:59.999999+02:00'
    print(f'Getting the upcoming {future_date} days events of your calendar')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          timeMax=a_week, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    with open('.calendar.json', 'w+') as f:
        json.dump(events, f)
    return events


def meetings_lists(events):
    which_meeting = input("Meeting name?: ")
    meetings = [item for item in events if item["summary"].lower() == which_meeting.lower()]
    if not meetings:
        print('No upcoming meetings found.')
    for meet in meetings:
        start = meet['start'].get('dateTime', meet['start'].get('date'))
        print(start, meet['summary'])
    calander_id = str()
    if len(meetings) > 1:
        meetin_time = input("Which meeting time would you like to choose? ")
        calander_id = meetings[int(meetin_time)-1]['id']
    elif len(meetings) == 1:
        calander_id = meetings[0]['id']
    else:
        print("There are no meetings")
        return service, ''
    return calander_id


def help_doctor():
    print('''
\033[1;32;4mAvailable Commands:\033[0m
create - Creating a new event
update - Update an existing event
meeting list - Displays your Google Calendar events for the next 7 days
delete - Delete an event
exit - Exits the Code Clinic program
''') 
    
    
def help_patient():
    print('''
\033[1;32;4mAvailable Commands:\033[0m    
join - Select an event that is available
meeting list - Displaying the users Google Calendar events
delete - Remove yourself from a slot
exit - Exits the code clinic program
''')
if __name__ == '__main__':
    user_name = user_name()
    role = which_role(user_name)
    action = what_would()
    service = creating_service()
    while handle_command(action, service, user_name, role):
        action = what_would()
