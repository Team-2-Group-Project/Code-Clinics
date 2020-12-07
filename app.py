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
            help_func()
        if action == "create":
            tttevent = event_maker.get_code_clinic_events(service, 7)
            primaryevent = event_maker.get_user_events(service, 7)
            calendar.generate_table(8,tttevent)
            calendar.generate_table(8,primaryevent)
            create.insert_details(service, user_name, tttevent, primaryevent)
            # create.insert_event(service, user_name, calendar.table_data, \
                # events, calendar.full_time_list)
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
            help_func()
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


def for_byron(service):
    tttevent = event_maker.get_code_clinic_events(service, 7)
    primaryevent = event_maker.get_user_events(service, 7)

def help_func():
    """
    Prints out the Help for the users to see what they can do, depending on their role
    """
    helped = """
        These are the code-clinics commands that can be used in various situations:\n\
        Please copy and paste the code in '<>' to call the functions:\n\
        \nlogging in and out:\n\
        login              Creates a log in session with you as the user\n\
            <python3 app.py login "username">\n\n\
        logout             logs you out of the code clinics calendar\n\
            <python3 app.py logout>\n\
        \n\
        \nVolunteering commands:\n\
        create                   Create a slot (of 3x30 minutes), to host a code-clinic\n\
            <python3 app.py create "summary" "description" "date" "time">\n\n\
        update                   Update an existing slots description/summary\n\
            <python3 app.py update "id" "summary" "description"\n\n\
        delete                   Delete a users sessions (of 3x30 minutes) code clinics\n\
            <python3 app.py delete "id">
        \n\
        \n\
        \nBooking commands:\n\
        join                      Join a code clinic slot (of 1x30 minutes) with a host\n\
            <python3 app.py join "host_username" "id_of_session" "description">\n\n\
        leave                     Leave a session that you are apart of\n\
            <python3 app.py leave "host_username" "id_of_session">\n\n\
        update                    Update the description with what you need help with\n\
            <python3 app.py update "host_username" "id_of_session" "description"\n\
        \n\
        \nCalendar commands:\n\
        volunteering_calendar     See the preview of the volunteering calendar as well as which slots are available\n\
            <python3 app.py "volunteering_calendar">\n\n\
        booking_calendar          See the preview of the booking calendar as well as which slots are available\n\
            <python3 app.py "booking_calendar">\n\n\
        
    """
    print(helped)
    return helped

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