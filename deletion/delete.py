
def delete_event(service, eventsID):
    """
    Takes in the event's ID in dictionary form "individual_time[0]['id']" as an argument, and then deletes that from the calendar
    """
    return service.events().delete(calendarId='primary',
                                   eventId=eventsID).execute()
