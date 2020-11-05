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
    time = re.findall(r"\d\d:\d\d", start_time)
    return time[0] if time else ''

def get_time():
    start_time = input("Please enter a start time (format: hh:mm): ")
    while start_time != valid_time(start_time):
        start_time = input("Please enter a start time (format: hh:mm): ")
    start_time = start_time.split(':')
    return start_time[0], start_time[1]

def insert_event(service):
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
    endtime = valid_slot + datetime.timedelta(minutes=30)
    endtime = str(endtime)
    endtime = endtime.split(" ")
    endtime = f'{endtime[0]}T{endtime[1]}+02:00'

    event = {
        'summary': input("What would you like to call this meeting? "),
        'location': '',
        'description': input("Please tell us what you need help with? "),
        'start': {
            'dateTime': starttime,
            'timeZone': 'Africa/Johannesburg',
        },
        'end': {
            'dateTime': endtime,
            'timeZone': 'Africa/Johannesburg',
        },
        "hangoutLink": "https://meet.google.com/snz-hfvt-zuo?pli=1&authuser=0",
        # 'attendees': [
        #     {'email': 'bthompso@student.wethinkcode.co.za'},
        # ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
        'anyoneCanAddSelf': True,
    }

    return service.events().insert(calendarId='primary', body=event).execute()