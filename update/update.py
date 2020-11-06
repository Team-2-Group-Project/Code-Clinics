def current_events(service, calander_id):
    event = service.events().get(calendarId='primary', eventId=calander_id).execute()

    return event


def update_event(service, calander_id):
    event = current_events(service, calander_id)


    event['summary'] = 'Appointment at Somasdsadsaewhere'

    try:
        updated_event = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()
        print(updated_event['updated'])
    except:
        print("No event with that name was found")

    return