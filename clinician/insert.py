# import re, datetime

# def valid_date(start_meet):
#     date = (re.findall(r"\d\d\d\d-\d\d-\d\d", start_meet))
#     return date[0] if date else ''


# def get_dates(date):
#     start_meet = date
#     start_meet = start_meet.split('-')
#     return start_meet[0], start_meet[1], start_meet[2]


# def valid_time(start_time):
#     time = re.findall("^\d\d:\d\d$", start_time)
#     return time[0] if time else ''


# def get_time(slot):
#     slots = slot.split(" - ")
#     if valid_time(slot[0]):
#         print("A Dalek appeared and stole that slot, call The Doctor!")
#     first = slots[0].split(":")
#     return first[0], first[1]


# def valid_date_checker(date, time_slot, slot):
#     year, month, day = get_dates(date)
#     hour, minute = get_time(time_slot)

#     valid_check = False

#     while not valid_check:
#         try:
#             valid_slot = datetime.datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute))
#             valid_check = True
#         except:
#             print("Please enter a valid date and time")
#             year, month, day = get_dates(date)
#             hour, minute = get_time(time_slot)

#     starttime = f'{year}-{month}-{day}T{hour}:{minute}:00+02:00'
#     endtime = str(valid_slot + datetime.timedelta(minutes=30)).split(" ")
#     endtime = f'{endtime[0]}T{endtime[1]}+02:00'

#     return starttime, endtime, valid_slot


# def slot_and_dates(td, meetings, all_c_slots):
#     # print(dates, slotted_time, user_selected_slot)

#     slots = {
#         1: "8:00 - 8:30",
#         2: "8:30 - 10:00",
#         3: "10:00 - 11:30",
#         4: "11:30 - 13:00",
#         5: "13:00 - 14:30",
#         6: "14:30 - 16:00",
#         7: "16:00 - 17:30",
#         8: "17:30 - 18:00",
#     }

#     # meetings
#     # meeting_num, startings = [], []
#     # for i in range(len(meetings)):
#     #     starttime = str(valid_slot + datetime.timedelta(minutes=(i) * 30)).split(" ")
#     #     meeting_num.append([item["id"] for item in meetings if item["start"]["dateTime"] == f'{starttime[0]}T{starttime[1]}+02:00'])
#     #     startings.append([item["start"]["dateTime"] for item in meetings if item["start"]["dateTime"] == f'{starttime[0]}T{starttime[1]}+02:00'])
#     #     # startings.append([item["start"]["dateTime"] for item in meetings if item["start"]["dateTime"] == f'{starttime[0]}T{starttime[1]}+02:00'])
#     # flatten_meetings = [item for sublist in meeting_num for item in sublist]
#     # flatten_starting = [item for sublist in startings for item in sublist]

#     # week_list = creating_list_of_week(8,datetime.date.today())
#     # time_list = []
#     # for i in range(len(flatten_starting)):
#     #     time_string = flatten_starting[i][:-9]
#     #     date_string = flatten_starting[i][:-15]
#     #     time_string = time_string[11:]
#     #     time_list.append(time_string)
#     # print("ts", time_list)
#     # time_index =  all_c_slots.index(time_list)
#     # date_index = week_list.index(date_string)
#     # slots.pop(time_index + 1)
#     # td[0].pop(date_index + 1)
#     # print(all_c_slots)

#     # print(flatten_meetings)
#     # print(flatten_starting)

#     counter = 1
#     td[0].pop(0)
#     for x in td[0]:
#         print(str(counter) + " : " + x)
#         counter += 1

#     print("_______________________________________________\n")

#     user_selected_date = input("Please select a date: ")
#     dates = td[0][int(user_selected_date)-1]
    
#     for x in slots:
#         print(str(x) + " : " + str(slots[x]))

#     user_selected_slot = input("Please select a slot: ")

#     slotted_time = slots.get(int(user_selected_slot))
#     return dates, slotted_time, user_selected_slot, slots


# def insertion_of_event(service, event):
#     try:
#         service.events().insert(calendarId='teamtwotesting@gmail.com', body=event, maxAttendees=2, sendUpdates='all', sendNotifications=True).execute()
#         return print("Event has been created")
#     except:
#         # print(e)
#         print("A spooky thing happened. Please try again.")


# def creating_list_of_week(i,today_date):
#     list_week = []
#     for i in range(i):
#         list_week.append(today_date + datetime.timedelta(days=i))
#         list_week[i] = list_week[i].strftime('%Y-%m-%d')
#     return list_week


# def insert_event(service, user_name, td, meetings, all_c_slots):
#     meetings = [item for item in meetings if item["creator"]["email"].lower() == user_name+'@student.wethinkcode.co.za']
#     # print(meetings)


#     dates, slotted_time, user_selected_slot, slots = slot_and_dates(td, meetings, all_c_slots)
#     starttime, endtime, valid_slot = valid_date_checker(dates, slotted_time, user_selected_slot)

#     sum_commdntline = input("What would you like to call this meeting? ")
#     dec_commdntline = input("Please tell us what you need help with? ")

#     event = {
#         'summary': sum_commdntline,
#         'location': '',
#         'description': dec_commdntline,
#         'start': {
#             'dateTime': starttime,
#             'timeZone': 'Africa/Johannesburg',
#         },
#         'end': {
#             'dateTime': endtime,
#             'timeZone': 'Africa/Johannesburg',
#         },
#         "hangoutLink": "https://meet.google.com/snz-hfvt-zuo?pli=1&authuser=0",
#         'attendees': [
#             {'email': f'{user_name}@student.wethinkcode.co.za'},
#         ],
#         'reminders': {
#             'useDefault': False,
#             'overrides': [
#                 {'method': 'email', 'minutes': 24 * 60},
#                 {'method': 'popup', 'minutes': 10},
#             ],
#         },
#         'anyoneCanAddSelf': True,
#     }

#     if int(user_selected_slot) == 1 or int(user_selected_slot) == 8:
#         insertion_of_event(service,event)
#     else:
#         for i in range(3):
#             starttime = str(valid_slot + datetime.timedelta(minutes=(i) * 30)).split(" ")
#             endtime = str(valid_slot + datetime.timedelta(minutes=(i + 1) * 30)).split(" ")
#             event["start"]["dateTime"] = f'{starttime[0]}T{starttime[1]}+02:00'
#             event["end"]["dateTime"] = f'{endtime[0]}T{endtime[1]}+02:00'
#             insertion_of_event(service, event)
#     return 


























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

def insert_event(command_params, service, user_name, table_data, full_time_list,\
    cc_events, us_events):
    date, time = validate_params(command_params)

    if validated_slot(table_data, date, time) == False:
        print("Invalid time slot, please stick to the allotted times, please check the calendar")
        return

    slots = user_pre_slotted(cc_events, user_name)
    if already_booked(slots, date, time) == False:
        print(f"You have already a time booked on '{date}' at '{time}'")
        return

    

    print("MORE VALIDATION")