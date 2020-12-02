#!/usr/bin/env python
import datetime, sys, json, os
from api_calls import serives_maker, event_maker
from user_logging import login, logout
from clinician import create, cancel, update
from patient import book, leave
from clinic_calendars import patient_calendar, clinician_calendar


def valid_action():
    return ["create", "update","meeting list","delete","exit","join","logout",'help']


def valid_command(action):
    """
    This function checks to make sure that the action from the user is valid and correct
    """
    if action in valid_action():
        return True
    else: 
        return False


def call_calendar(events, calendar):
    """
    This function calls the calendar if the user has meetings in it \
        to print and generate it
    """
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
            help_func("c")
        if action == "create":
            events = event_maker.get_user_events(service, 7)
            calendar.generate_table(8,events)
            create.insert_event(service, user_name, calendar.table_data, \
                events, calendar.full_time_list)
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
            cancel.delete_event(service, user_name, calendar.table_data, \
                events, calendar.full_time_list)
            calendar.table_data = []
        elif action == "exit":
            print("Thank you for using code clinic")
            return False
    if role == 'p' or role == 'patient':
        if action == 'help':
            help_func("p")
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
    """
    This function is used to find and isolate an individual meeting slot \
        and then return that sepcific meetings ID
    """
    which_meeting = input("Meeting name?: ")
    meetings = [item for item in events if \
        item["summary"].lower() == which_meeting.lower()]
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


def help_func(role):
    """
    Prints out the Help for the users to see what they can do, depending on their role
    """
    if role == "c":
        print('''
            \033[1;32;4mAvailable Commands:\033[0m\
            \ncreate - Creating a new event\
            \nupdate - Update an existing event\
            \nmeeting list - Displays your Google Calendar events for the next 7 days\
            \ndelete - Delete an event\
            \nexit - Exits the Code Clinic program\
            ''') 
    elif role == "p":
        print('''\n\033[1;32;4mAvailable Commands:\033[0m\n\
            \njoin - Select an event that is available\
            \nmeeting list - Displaying the users Google Calendar events\
            \ndelete - Remove yourself from a slot\
            \nexit - Exits the code clinic program\
            ''')
    return

def for_byron(service):
    tttevent = event_maker.get_code_clinic_events(service, 7)
    primaryevent = event_maker.get_user_events(service, 7)

    print("tttevent: ", tttevent)
    print("primaryevent: ", primaryevent)



def main():
    """
    This is the main function where everything is first called and processed
    """


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
    for_byron(service)
    handle_command(action, service, user_name, role)


if __name__ == '__main__':
    main()