def current_events(service, calander_id):
    event = service.events().get(calendarId='primary', eventId=calander_id).execute()

    return event

def delete_event(service, calander_id, user_name):
    event = current_events(service, calander_id)

    # print(event)

    # meetings = [item for item in event if item["email"].lower() == user_name+'@student.wethinkcode.co.za']
    # print(meetings)

    count = 0
    for i in event['attendees']:
        if i['email'] != user_name+'@student.wethinkcode.co.za':
            count += 1
            continue
        else:
            event['attendees'].pop(count)
        count += 1

    try:
        updated_event = service.events().update(calendarId='primary', eventId=event['id'], body=event, maxAttendees=2, sendUpdates='all', sendNotifications=True, alwaysIncludeEmail=True).execute()
        print("You have been removed")
    except:
        print("No event with that name was found")

    return