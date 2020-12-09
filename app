#!/usr/bin/env python3
import datetime, sys, json, os
from api_calls import serives_maker, event_maker
from user_logging import login, logout
from clinician import create, cancel, update
from patient import book, leave
from clinic_calendars import patient_calendar, clinician_calendar


def valid_action():
    return ["create", "cancel", "update", "meeting_list","join", "leave","logout",'help']


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
# def handle_command(action, service, user_name, role):
    '''
    Creating conditions that will take the users input
    , then performing the requested action
    '''
    #THIS LINE IS TO BE DELETED ONCE WE REMOVE ROLES
    calendar = clinician_calendar if role == "c" else patient_calendar


    if command == "help":
        help_func()
        return
    #./app create 2020-12-09 08:00
    #./app cancel 'id-start-event'
    # print(command)
    # print(command_params)
    # print(service)
    # print(user_name)

    if command == "create":
        events = event_maker.get_user_events(service, 7)
        calendar.generate_table(8,events)
        create.insert_event(command_params, service, user_name,calendar.table_data, calendar.full_time_list)
        calendar.table_data = []
    elif command == "cancel":
        events = event_maker.get_user_events(service, 7)
        calendar.print_table(8, events)
        calendar.generate_table(8,events)
        cancel.delete_event(service, user_name, calendar.table_data, \
            events, calendar.full_time_list)
        calendar.table_data = []
    elif command == "update":
        events = event_maker.get_user_events(service, 7)
        call_calendar(events, calendar,service,user_name)
        calander_id = meetings_lists(events)
        update.update_event(service, calander_id)
    elif command == "meeting_list":
        events = event_maker.get_user_events(service, 7)
        calendar.print_table(8, events)
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
    
    return

    # calendar = clinician_calendar if role == "c" else patient_calendar
    # if action not in valid_action() and not 'join' in action: 
    #     print("Invalid command")
    #     sys.exit()
    # if role == 'c' or role == 'clinician':
    #     if action == 'help':
    #         help_func()
    #     if action == "create":
    #         events = event_maker.get_user_events(service, 7)
    #         calendar.generate_table(8,events)
    #         create.insert_event(service, user_name, calendar.table_data, \
    #             events, calendar.full_time_list)
    #         calendar.table_data = []
    #     elif action == "update":
    #         events = event_maker.get_user_events(service, 7)
    #         call_calendar(events, calendar)
    #         calander_id = meetings_lists(events)
    #         update.update_event(service, calander_id)
    #     elif action == "meeting list":
    #         events = event_maker.get_user_events(service, 7)
    #         calendar.print_table(8, events)
    #     elif action == "delete":
    #         events = event_maker.get_user_events(service, 7)
    #         calendar.print_table(8, events)
    #         calendar.generate_table(8,events)
    #         cancel.delete_event(service, user_name, calendar.table_data, \
    #             events, calendar.full_time_list)
    #         calendar.table_data = []
    #     elif action == "exit":
    #         print("Thank you for using code clinic")
    #         return False
    # if role == 'p' or role == 'patient':
    #     if action == 'help':
    #         help_func()
    #     if 'join' in action:
    #         events = event_maker.get_user_events(service, 7)
    #         call_calendar(events, calendar,service,user_name)
    #         #calander_id = meetings_lists(events)
    #         book.insert_patient(service, action.split()[1], user_name)
    #     elif action == "update":
    #         events = event_maker.get_user_events(service, 7)
    #         call_calendar(events, calendar,service,user_name)
    #         calander_id = meetings_lists(events)
    #     elif action == "meeting list":
    #         events = event_maker.get_user_events(service, 7)
    #         call_calendar(events, calendar,service,user_name)
    #     elif action == "delete":
    #         events = event_maker.get_user_events(service, 7)
    #         call_calendar(events, calendar,service,user_name)
    #         calander_id = meetings_lists(events)
    #         leave.delete_event(service, calander_id, user_name)
    #     elif action == "exit":
    #         print("Thank you for using code clinic")
    #         return False
    # return True


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
   delete                    Delete a users sessions (of 3x30 minutes) code clinics         \
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

    actions = action.split(" ")
    command = ""
    params = ""
    for comms in actions:
        if comms in valid_action():
            command = comms

    if not command == "":
        actions.pop(action.index(command))
        params = list(map(lambda x: x.lower(), actions))
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
