#!/usr/bin/env python
import datetime, sys, json, os
from api_calls import serives_maker, event_maker
from user_logging import login, logout
from clinician import create, cancel, update
from patient import book, leave
from clinic_calendars import patient_calendar, clinician_calendar


def valid_action():
    return ["create", "update","meeting list","delete","exit","join","logout",'help']


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
    if action in valid_action():
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
    calendar = clinician_calendar if role == "c" else patient_calendar
    if action not in valid_action(): 
        print("Invalid command")
        sys.exit()
    if role == 'c' or role == 'clinician':
        if action == 'help':
            help_doctor()
        if action == "create":
            events = event_maker.get_user_events(service, 7)
            calendar.generate_table(8,events)
            create.insert_event(service, user_name, calendar.table_data, events, calendar.full_time_list)
            calendar.table_data = []
        elif action == "update":
            events = event_maker.get_user_events(service, 7)
            call_calendar(events, calendar)
            calander_id = meetings_lists(events)
            update.update_event(service, calander_id)
        elif action == "meeting list":
            events = event_maker.get_user_events(service, 7)
            calendar.print_table(8, events)
        elif action == "delete":
            events = event_maker.get_user_events(service, 7)
            calendar.print_table(8, events)
            calendar.generate_table(8,events)
            cancel.delete_event(service, user_name, calendar.table_data, events, calendar.full_time_list)
            calendar.table_data = []
        elif action == "exit":
            print("Thank you for using code clinic")
            return False
    if role == 'p' or role == 'patient':
        if action == 'help':
            help_patient()
        if action == "join":
            events = event_maker.get_user_events(service, 7)
            call_calendar(events, calendar)
            calander_id = meetings_lists(events)
            book.insert_patient(service, calander_id, user_name)
        elif action == "update":
            events = event_maker.get_user_events(service, 7)
            call_calendar(events, calendar)
            calander_id = meetings_lists(events)
        elif action == "meeting list":
            events = event_maker.get_user_events(service, 7)
            call_calendar(events, calendar)
        elif action == "delete":
            events = event_maker.get_user_events(service, 7)
            call_calendar(events, calendar)
            calander_id = meetings_lists(events)
            leave.delete_event(service, calander_id, user_name)
        elif action == "exit":
            print("Thank you for using code clinic")
            return False
    return True


def arguments():
    arg = sys.argv
    arg = ' '.join(arg[1:])
    return arg


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
    action = arguments()
    print(action)
    if action == 'logout':
        print(("\033[1;32mLogging out\033[0m"))
        logout.logout()
        sys.exit()
    else:
        print(("\033[1;32mWelcome to Code Clinic!\033[0m"))
    user_name,role = login.log_in_checker()
    service = serives_maker.creating_service()
    handle_command(action, service, user_name, role)