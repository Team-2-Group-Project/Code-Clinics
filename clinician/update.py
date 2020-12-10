def current_events(service, calander_id):
    event = service.events().get(calendarId='teamtwotesting@gmail.com', eventId=calander_id).execute()
    return event

def updaters(service, event):
    try:
        service.events().update(calendarId='teamtwotesting@gmail.com', eventId=event['id'], body=event, maxAttendees=2, sendUpdates='all', sendNotifications=True, alwaysIncludeEmail=True).execute()
        print("Your event has been updated")
    except:
        print("No event with that ID was found")

def update_event(service, params, events, user_name):
    event = current_events(service, params[0])

    summary = event["summary"]
    description = event["description"]
    if len(params) == 3:
        summary = params[1]
        description = params[2]
    event['summary'] = summary
    event['description'] = description

    if (event["creator"]['email']) == (user_name + '@student.wethinkcode.co.za'):
        if (event["id"]) == params[0]:
            updaters(service, event)
            return
        else:
            print("The ID's do not match, please try again.")
    else:
        print("This is not your slot, please choose your own slot.")


    return