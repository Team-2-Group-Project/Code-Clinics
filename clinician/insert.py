import re, datetime

def valid_date(start_date):
    if (re.findall(r"\d\d\d\d-\d\d-\d\d", start_date)):
        return True
    else:
        return False

def valid_time(start_time):
    if re.findall(r"^\d\d:\d\d$", start_time):
        return True
    else:
        return False

def validate_params(command_params):
    if command_params == []:
        print("invalid request, plese try again")
        return "", ""
    if len(command_params) != 2:
        print("invalid request, plese try again")
        return "", ""

    date = command_params[0]
    time = command_params[1]
    
    if valid_date(date) == True and valid_time(time) == True:
        return date, time
    else:
        print("invalid request, plese try again")
        return "", ""

    return "", ""

def meeting_setups(command_params):
    summary = command_params[0]
    description = command_params[1]
    return summary, description

def clearing_dates(table_data):
    available_dates = table_data[0]
    available_dates.pop(available_dates.index(""))
    return available_dates

def validated_slot(table_data, date, time):
    start_times = ['08:00', '08:30', '10:00', '11:30', '13:00', '14:30', '16:00', '17:30']
    available_dates = clearing_dates(table_data)
    time_in = False
    date_in = False
    for i in start_times:
        if time == str(i):
            time_in = True
            break

    for i in available_dates:
        if date == str(i):
            date_in = True
            break

    if time_in == True and date_in == True:
        return True
    else:
        return False

def user_pre_slotted(cc_events, user_name):
    creators = list()
    start_times = list()
    for i in range(len(cc_events)):
        creators.append(cc_events[i]['creator']['email'])
        start_times.append(cc_events[i]['start']['dateTime'])

    creator_names = list()
    for i in range(len(creators)):
        name = creators[i]
        name = name.split('@')
        creator_names.append(name[0])

    slots = [cc_events[num]['start']['dateTime'] for num, user in enumerate(creator_names) if creator_names[num] == user_name]
    return slots

def already_booked(slots, date, time):
    date_time = f'{date}T{time}:00+02:00'
    conflicted_times = ''
    for i in slots:
        if date_time == i:
            conflicted_times = i
            break
    
    if conflicted_times != '':
        return False
    else:
        return True

def make_datetime_from_string(string):
    """
    Creates a dattime object form a given string
    Parameter:  string (yyy-mm-ddTHH:MM:00+0200)
    Returns:    datetime object
    """
    return datetime.datetime.strptime(string, "%Y-%m-%dT%H:%M:%S%z")

def freebusy_check(service, date, time, user_name):
    """
    Needs to be in the ISO FORMAT for it to work properly...
    """
    event = {
        "timeMin": (make_datetime_from_string(f'{date}T{time}:00+0200')).isoformat(),
        "timeMax": (make_datetime_from_string(f'{date}T{time}:00+0200')+datetime.timedelta(minutes = 90)).isoformat(),
        "timeZone": 'Africa/Johannesburg',
        "items": [
            {
                "id": user_name + '@student.wethinkcode.co.za'
            },
            {
                'id': 'teamtwotesting@gmail.com'
            }
        ]
    }

    eventsResult = service.freebusy().query(body=event).execute()
    return eventsResult

def do_you_have_meetings(service, date, time, user_name):
    events = freebusy_check(service, date, time, user_name)
    two_cals = events['calendars']
    patient, clinic = two_cals[user_name+'@student.wethinkcode.co.za'], two_cals['teamtwotesting@gmail.com']

    if patient['busy'] == []:
        return True
    else:
        return False
    return False

def insertion_of_event(service, event):
    try:
        service.events().insert(calendarId='teamtwotesting@gmail.com', body=event, maxAttendees=2, sendUpdates='all', sendNotifications=True).execute()
        return print("Event has been created")
    except:
        print("A spooky thing happened. Please try again.")

def valid_date_checker(date, time):
    date = date.split("-")
    time = time.split(":")
    year, month, day = date[0], date[1], date[2]
    hour, minute = time[0], time[1]
    valid_check = False

    while not valid_check:
        try:
            valid_slot = datetime.datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute))
            valid_check = True
        except:
            print("Please enter a valid date and time")

    starttime = f'{year}-{month}-{day}T{hour}:{minute}:00+02:00'
    endtime = str(valid_slot + datetime.timedelta(minutes=30)).split(" ")
    endtime = f'{endtime[0]}T{endtime[1]}+02:00'

    return starttime, endtime, valid_slot

def create_event(date, time, summary, description, user_name, service):
    
    starttime, endtime, valid_slot = valid_date_checker(date, time)
    
    event = {
        'summary': summary,
        'location': '',
        'description': description,
        'start': {
            'dateTime': starttime,
            'timeZone': 'Africa/Johannesburg',
        },
        'end': {
            'dateTime': endtime,
            'timeZone': 'Africa/Johannesburg',
        },
        "hangoutLink": "https://meet.google.com/snz-hfvt-zuo?pli=1&authuser=0",
        'attendees': [
            {'email': f'{user_name}@student.wethinkcode.co.za'},
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
        'anyoneCanAddSelf': True,
    }

    if time == '08:00' or time == '17:30':
        insertion_of_event(service,event)
    else:
        for i in range(3):
            starttime = str(valid_slot + datetime.timedelta(minutes=(i) * 30)).split(" ")
            endtime = str(valid_slot + datetime.timedelta(minutes=(i + 1) * 30)).split(" ")
            event["start"]["dateTime"] = f'{starttime[0]}T{starttime[1]}+02:00'
            event["end"]["dateTime"] = f'{endtime[0]}T{endtime[1]}+02:00'
            insertion_of_event(service, event)
    return 

def insert_event(command_params, service, user_name, table_data, full_time_list, cc_events, us_events):
    date, time = validate_params(command_params[:2])
    summary, description = meeting_setups(command_params[2:])

    if validated_slot(table_data, date, time) == False:
        print("Invalid time slot, please stick to the allotted times, please check the calendar.")
        return

    slots = user_pre_slotted(cc_events, user_name)
    if already_booked(slots, date, time) == False:
        print(f"You have already a time booked on '{date}' at '{time}'.")
        return

    if do_you_have_meetings(service, date, time, user_name) == False:
        print("You already have a meeting at this time in your calendar.")
        return
    
    create_event(date, time, summary, description, user_name, service)
