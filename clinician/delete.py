import re, datetime

def valid_date(start_meet):
    date = (re.findall(r"\d\d\d\d-\d\d-\d\d", start_meet))
    return date[0] if date else ''


def get_dates(date):
    start_meet = date
    start_meet = start_meet.split('-')
    return start_meet[0], start_meet[1], start_meet[2]


def valid_time(start_time):
    time = re.findall("^\d\d:\d\d$", start_time)
    return time[0] if time else ''


def get_time(slot):
    slots = slot.split(" - ")
    if valid_time(slot[0]):
        print("A Dalek appeared and stole that slot, call The Doctor!")
    first = slots[0].split(":")
    return first[0], first[1]


def valid_date_checker(date, time_slot, slot):
    year, month, day = get_dates(date)
    hour, minute = get_time(time_slot)

    valid_check = False

    while not valid_check:
        try:
            valid_slot = datetime.datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute))
            valid_check = True
        except:
            print("Please enter a valid date and time")
            year, month, day = get_dates(date)
            hour, minute = get_time(time_slot)

    starttime = f'{year}-{month}-{day}T{hour}:{minute}:00+02:00'
    endtime = str(valid_slot + datetime.timedelta(minutes=30)).split(" ")
    endtime = f'{endtime[0]}T{endtime[1]}+02:00'

    return starttime, endtime, valid_slot


def slot_and_dates(td, meetings, all_c_slots):
    # print(dates, slotted_time, user_selected_slot)

    slots = {
        1: "8:00 - 8:30",
        2: "8:30 - 10:00",
        3: "10:00 - 11:30",
        4: "11:30 - 13:00",
        5: "13:00 - 14:30",
        6: "14:30 - 16:00",
        7: "16:00 - 17:30",
        8: "17:30 - 18:00",
    }

    # meetings
    # meeting_num, startings = [], []
    # for i in range(len(meetings)):
    #     starttime = str(valid_slot + datetime.timedelta(minutes=(i) * 30)).split(" ")
    #     meeting_num.append([item["id"] for item in meetings if item["start"]["dateTime"] == f'{starttime[0]}T{starttime[1]}+02:00'])
    #     startings.append([item["start"]["dateTime"] for item in meetings if item["start"]["dateTime"] == f'{starttime[0]}T{starttime[1]}+02:00'])
    #     # startings.append([item["start"]["dateTime"] for item in meetings if item["start"]["dateTime"] == f'{starttime[0]}T{starttime[1]}+02:00'])
    # flatten_meetings = [item for sublist in meeting_num for item in sublist]
    # flatten_starting = [item for sublist in startings for item in sublist]

    # week_list = creating_list_of_week(8,datetime.date.today())
    # time_list = []
    # for i in range(len(flatten_starting)):
    #     time_string = flatten_starting[i][:-9]
    #     date_string = flatten_starting[i][:-15]
    #     time_string = time_string[11:]
    #     time_list.append(time_string)
    # print("ts", time_list)
    # time_index =  all_c_slots.index(time_list)
    # date_index = week_list.index(date_string)
    # slots.pop(time_index + 1)
    # td[0].pop(date_index + 1)
    # print(all_c_slots)

    # print(flatten_meetings)
    # print(flatten_starting)

    counter = 1
    td[0].pop(0)
    for x in td[0][:8]:
        print(str(counter) + " : " + x)
        counter += 1

    print("_______________________________________________\n")

    user_selected_date = input("Please select a date: ")
    dates = td[0][int(user_selected_date)-1]
    
    for x in slots:
        print(str(x) + " : " + str(slots[x]))

    user_selected_slot = input("Please select a slot: ")

    slotted_time = slots.get(int(user_selected_slot))
    return dates, slotted_time, user_selected_slot, slots


def deleted(service, eventsID):
    try:
        service.events().delete(calendarId='teamtwotesting@gmail.com',
                                   eventId=eventsID).execute()
        print("Your event has been deleted")
    except:
        print("That is not an existing event")


def delete_event(service, user_name, td, meetings, all_c_slots):
    """
    Takes in the event's ID in dictionary form "individual_time[0]['id']" as an argument, and then deletes that from the calendar
    """
    meetings = [item for item in meetings if item["creator"]["email"].lower() == user_name+'@student.wethinkcode.co.za']

    dates, slotted_time, user_selected_slot, slots = slot_and_dates(td, meetings, all_c_slots)
    starttime, endtime, valid_slot = valid_date_checker(dates, slotted_time, user_selected_slot)

    slots_to_delete = 1
    if user_selected_slot != '1':
        slots_to_delete = 3

    meeting_num = []
    for i in range(slots_to_delete):
        starttime = str(valid_slot + datetime.timedelta(minutes=(i) * 30)).split(" ")
        meeting_num.append([item["id"] for item in meetings if item["start"]["dateTime"] == f'{starttime[0]}T{starttime[1]}+02:00'])
    flatten_meetings = [item for sublist in meeting_num for item in sublist]

    if int(user_selected_slot) == 1 or int(user_selected_slot) == 8:
        deleted(service, flatten_meetings[0])
    else:
        for i in range(3):
            deleted(service, flatten_meetings[i])
    return