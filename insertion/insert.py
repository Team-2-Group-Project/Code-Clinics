import re, datetime

def valid_date(start_meet):
    date = (re.findall(r"\d\d\d\d-\d\d-\d\d", start_meet))
    print(date)
    # valid_day = date[0].split('-')
    # valid_day = list(map(int, valid_day))
    # yay = datetime.datetime(year=valid_day[0], month=valid_day[1],day=valid_day[2])
    return date[0] if date else ''

def get_dates():
    start_meet = input("Please choose a date for your meeting (format: yyyy-mm-dd): ")
    while start_meet != valid_date(start_meet):
        start_meet = input("Please choose a date for your meeting (format: yyyy-mm-dd): ")
    start_meet = start_meet.split('-')
    return start_meet[0], start_meet[1], start_meet[2]

def valid_time(start_time):
    date = re.findall(r"\d\d:\d\d", start_time)

def get_time():
    start_time = input("Please enter a start time (format: hh:mm): ")
    while start_time != valid_time(start_time):
        start_time = input("Please enter a start time (format: hh:mm): ")


# if start_meet in months_abbr or start_meet in months_names or start_meet in range(1,13):

# year = input("please input a year: ")
# month = input("please input a month: ")
# day = input("please input a day: ")
# hour = input("please input a hour: ")
# minutes = input("please input a minutes: ")


# print(f"{year}-{month}-{day}T{hour}:{minutes}:00+02:00")

def insert_event(service):
    year, month, day = get_dates()
    hour, minute = get_time()

    print(f"{year}-{month}-{day}T{hour}:{minute}:00+02:00")

#     event = {
#         'summary': input("What would you like to call this meeting? "),
#         'location': '',
#         'description': input("Please tell us what you need help with? "),
#         'start': {
#             'dateTime': "2020-11-05T13:00:00+02:00",
#             'timeZone': 'Africa/Johannesburg',
#         },
#         'end': {
#             'dateTime': '2020-11-05T13:30:00+02:00',
#             'timeZone': 'Africa/Johannesburg',
#         },
#         "hangoutLink": "https://meet.google.com/snz-hfvt-zuo?pli=1&authuser=0",
#         # 'attendees': [
#         #     {'email': 'bthompso@student.wethinkcode.co.za'},
#         # ],
#         'reminders': {
#             'useDefault': False,
#             'overrides': [
#                 {'method': 'email', 'minutes': 24 * 60},
#                 {'method': 'popup', 'minutes': 10},
#             ],
#         },
#         'anyoneCanAddSelf': True,
#     }

    # return service.events().insert(calendarId='primary', body=event).execute()
