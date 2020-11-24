def current_events(service, calander_id):
    event = service.events().get(calendarId='primary', eventId=calander_id).execute()

    return event

def insert_patient(service, calander_id, user_name):
    event = current_events(service, calander_id)

    event['attendees'].append({'email': f'{user_name}@student.wethinkcode.co.za'})

    try:
        service.events().update(calendarId='primary', eventId=event['id'], body=event, maxAttendees=2, sendUpdates='all', sendNotifications=True, alwaysIncludeEmail=True).execute()
        print("You have successfully joined the meeting")
    except:
        print("No event with that name was found")

    return