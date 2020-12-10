def current_events(service, calander_id):
    event = service.events().get(calendarId='teamtwotesting@gmail.com', eventId=calander_id).execute()

    return event


def leaving(service, event):
    try:
        service.events().update(calendarId='teamtwotesting@gmail.com', eventId=event['id'], body=event, maxAttendees=2, sendUpdates='all', sendNotifications=True, alwaysIncludeEmail=True).execute()
        print("You have left the meeting.")
    except:
        print("No event with that name was found.")


def delete_event(service, params, user_name):
    event = current_events(service, params)
    count = 0
    for i in event['attendees']:
        if i['email'] != user_name+'@student.wethinkcode.co.za':
            count += 1
            continue

    if count != 0:
        if (event["id"]) == params:
            event['attendees'].pop(count)
            leaving(service, event)
        else:
            print("The ID's do not match, please try again.")
    else:
        print("This is not your slot, please choose your own slot.")