import re, datetime

def valid_date(start_meet):
    date = (re.findall(r"\d\d\d\d-\d\d-\d\d", start_meet))
    return date[0] if date else ''

def get_dates():
    start_meet = input("Please choose a date for your meeting (format: yyyy-mm-dd): ")
    while start_meet != valid_date(start_meet):
        start_meet = input("Please choose a date for your meeting (format: yyyy-mm-dd): ")
    start_meet = start_meet.split('-')
    return start_meet[0], start_meet[1], start_meet[2]

def valid_time(start_time):
    time = re.findall("^\d\d:\d\d$", start_time)
    return time[0] if time else ''

def get_time():
    start_time = input("Please enter a start time (format: hh:mm): ")
    while start_time != valid_time(start_time):
        start_time = input("Please enter a start time (format: hh:mm): ")
    start_time = start_time.split(':')
    return start_time[0], start_time[1]


def valid_date_checker():
    year, month, day = get_dates()
    hour, minute = get_time()

    valid_check = False
    while not valid_check:
        try:
            valid_slot = datetime.datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute))
            valid_check = True
        except:
            print("Please enter a valid date and time")
            year, month, day = get_dates()
            hour, minute = get_time()


    starttime = f'{year}-{month}-{day}T{hour}:{minute}:00+02:00'
    endtime = str(valid_slot + datetime.timedelta(minutes=30)).split(" ")
    endtime = f'{endtime[0]}T{endtime[1]}+02:00'

    return starttime, endtime


def current_events(service, calander_id):
    event = service.events().get(calendarId='primary', eventId=calander_id).execute()

    return event


def what_to_update():
    to_update = []
    possible_options = ['done', 'summary', 'description', 'start']
    print("(Please choose done when you are finished)\npossible options: ", end=" ")
    for i in possible_options:
        if i == possible_options[-1]:
            print(i, end="\n")
            break
        print(f"{i} |", end=" ")
    while 'done' not in to_update:
        user_option = input("What would you like to update?: ").lower()
        if user_option not in possible_options:
            print("This is not a possible option, please try again!")
            continue
        to_update.append(user_option)

    if 'done' in to_update:
        to_update.pop(to_update.index('done'))

    return to_update

def update_event(service, calander_id):
    event = current_events(service, calander_id)


    # while response != nothing:
        # input("what would you like to update? ")


    to_update = what_to_update()
    # print(to_update)

    # starttime, endtime = valid_date_checker()

    for i in to_update:
        if i == 'start':
            starttime, endtime = valid_date_checker()
            event[i]['dateTime'] = starttime
            event['end']['dateTime'] = endtime
            continue
        event[i] = input(f"Please provide a new \"{i.capitalize()}\": ")

    try:
        updated_event = service.events().update(calendarId='primary', eventId=event['id'], body=event, maxAttendees=2, sendUpdates='all', sendNotifications=True, alwaysIncludeEmail=True).execute()
        print("Your event has been updated")
    except:
        print("No event with that name was found")

    return
