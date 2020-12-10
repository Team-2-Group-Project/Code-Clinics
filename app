#!/usr/bin/env python3
import datetime, sys, json, os, re
from api_calls import serives_maker, event_maker
from user_logging import login, logout
from clinician import create, cancel, update
from patient import book, leave
from clinic_calendars import patient_calendar, clinician_calendar, delete_calendar

def valid_action():
    return ["create", "cancel", "update", "join", "leave","logout",'help','create_calendar_slot','join_calendar_slot','delete_calendar_slot']


def valid_command(action):
    """
    This function checks to make sure that the action from the user is valid and correct
    """
    if action in valid_action():
        return True
    else:
        return False


def call_calendar(events, calendar,service,user_name):
    """
    This function calls the calendar if the user has meetings in it \
        to print and generate it
    """
    try:
        calendar.generate_table(8,events, fetch_calendar(service),user_name)
        calendar.table_data = []
    except:
        print("You have no meetings in your calendar")


def handle_command(command, command_params, service, user_name, role):
    '''
    Creating conditions that will take the users input, then performing the requested action
    '''

    if command == "help":
        help_func()
        return

    if command == "create":
        print("Attempting to create event(s)...")
        us_events = event_maker.get_user_events(service, 7)
        cc_events = event_maker.get_code_clinic_events(service, 7) 
        clinician_calendar.generate_table(8, us_events, user_name)
        create.insert_event(command_params, service, user_name, clinician_calendar.table_data, clinician_calendar.full_time_list, cc_events, us_events)
        return

    elif command == "cancel":
        print("Attempting to delete your event...")
        events = event_maker.get_user_events(service, 7)
        cancel.delete_event(command_params, service, user_name, events)
        return

    elif command == "update":
        print("Attempting to update your event...")
        events = event_maker.get_user_events(service, 7)
        update.update_event(service, command_params, events, user_name)
        return

    elif command == 'join_calendar_slot':
        events = event_maker.get_user_events(service, 7)
        try:
            patient_calendar.generate_table(8,events, fetch_calendar(service),user_name)
            patient_calendar.table_data = []
        except:
            print("You have no meetings in your calendar")

    elif command == 'delete_calendar_slot':
        events = event_maker.get_user_events(service, 7)
        try:
            delete_calendar.generate_table(8,fetch_calendar(service),user_name)
            delete_calendar.table_data = []
        except:
            print("You have no meetings in your calendar")

    elif command == 'create_calendar_slot':
        events = event_maker.get_user_events(service, 7)
        try:
            clinician_calendar.print_table(8, events,user_name)
        except:
            print('You have no meetings in your calendar')

    elif command == "join":
        events = event_maker.get_user_events(service, 7)
        call_calendar(events, calendar,service,user_name)
        #calander_id = meetings_lists(events)
        # book.insert_patient(service, action.split()[1], user_name)

    elif command == "leave":
        events = event_maker.get_user_events(service, 7)
        call_calendar(events, calendar,service,user_name)
        calander_id = meetings_lists(events)
        leave.delete_event(service, calander_id, user_name)
    
    
    elif command == "leave":
        events = event_maker.get_user_events(service, 7)
        call_calendar(events, calendar,service,user_name)
        calander_id = meetings_lists(events)
        leave.delete_event(service, calander_id, user_name)
       
    return


def arguments():
    arg = sys.argv
    arg = arg[1:]
    return arg


def fetch_calendar(service):
    tttevent = event_maker.get_code_clinic_events(service, 7)
    primaryevent = event_maker.get_user_events(service, 7)

    return tttevent
   

def help_func():
    """
    Prints out the Help for the users to see what they can do, depending on their role
    """
    helped = """
   These are the code-clinics commands that can be used in various situations:\n\
   Please copy and paste the code in '<>' to call the functions:\n\
   \nlogging in and out:\n\
   login                     Creates a log in session with you as the user                  \
   <python3 app.py login "username">
   logout                    logs you out of the code clinics calendar                      \
   <python3 app.py logout>
   \nVolunteering commands:\n\
   create                    Create a slot (of 3x30 minutes), to host a code-clinic         \
   <python3 app.py create "summary" "description" "date" "time">
   update                    Update an existing slots description/summary                   \
   <python3 app.py update "id" "summary" "description">
   delete                    Deletes an individual users sessions of code clinics           \
   <python3 app.py delete "id">
   \nBooking commands:\n\
   join                      Join a code clinic slot (of 1x30 minutes) with a host          \
   <python3 app.py join "host_username" "id_of_session" "description">
   leave                     Leave a session that you are apart of                          \
   <python3 app.py leave "host_username" "id_of_session">
   update                    Update the description with what you need help with            \
   <python3 app.py update "host_username" "id_of_session" "description"
   \nCalendar commands:\n\
   voluntee_calendar     See a preview of the volunteering calendar, and the available slots\
   <python3 app.py "voluntee_calendar">
   booking_calendar          See a preview of the booking calendar, and the available slots \
   <python3 app.py "booking_calendar"> 
   """
    print(helped)
    return helped


def argument_validator(action):
    """
    Recievs the action from the user as a parameter, and then it splits them\
        valids that it is a valid argument and the parameters are valid
    :returns: command (being the valid action to take), lower case
    :returns: all the params for the argument, lower case
    """
    command = ""
    params = ""
    if action[0] in valid_action():
        command = action[0]

    if not command == "":
        action.pop(action.index(command))
        params = list(map(lambda x: x.lower(), action))
    elif command in valid_action() and params == "":
        print("no valid parameteres found, plese try again")
        help_func()
        return "", ""
    else:
        print("no valid action found, please try again")
        help_func()
        return "", ""

    return command.lower(), params


def main():
    """
    This is the main function where everything is first called and processed
    """

    action = arguments()
    command, command_params = argument_validator(action)
    if command == "" and command_params == "":
        return
    if command == 'logout':
        print(("\033[1;32mLogging out\033[0m"))
        logout.logout()
        sys.exit()
    # else:
    #     print(("\033[1;32mWelcome to Code Clinic!\033[0m"))
    user_name, role = login.log_in_checker()
    service = serives_maker.creating_service()
    # handle_command(action, service, user_name, role)
    handle_command(command, command_params, service, user_name, role)


if __name__ == '__main__':
    main()