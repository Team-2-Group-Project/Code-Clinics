def current_events(service, calander_id):
    event = service.events().get(calendarId='primary', eventId=calander_id).execute()

    return event

def delete_event(service, calander_id, user_name):
    event = current_events(service, calander_id)

    event['attendees'] = []

    print(event)

    try:
        updated_event = service.events().update(calendarId='primary', eventId=event['id'], body=event, maxAttendees=2, sendUpdates='all', sendNotifications=True, alwaysIncludeEmail=True).execute()
        print(updated_event['updated'])
    except:
        print("No event with that name was found")

    return