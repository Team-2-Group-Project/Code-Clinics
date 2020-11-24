
def delete_event(service, eventsID):
    """
    Takes in the event's ID in dictionary form "individual_time[0]['id']" as an argument, and then deletes that from the calendar
    """
    try:
        service.events().delete(calendarId='primary',
                                   eventId=eventsID).execute()
        print("Your event has been deleted")
    except:
        print("That is not an existing event")

    return