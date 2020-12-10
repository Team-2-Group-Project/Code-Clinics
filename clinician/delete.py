def deleted(service, eventsID):
    try:
        service.events().delete(calendarId='teamtwotesting@gmail.com',
                                   eventId=eventsID).execute()
        print("Your event has been deleted")
    except:
        print("That is not an existing event")

def delete_event(delete_id ,service, user_name, events):
    delete_id = ''.join(delete_id)
    canllelation = [item for item in events if item["id"] == delete_id]
    if (canllelation[0]["creator"]['email']) == (user_name + '@student.wethinkcode.co.za'):
        if (canllelation[0]["id"]) == delete_id:
            deleted(service, delete_id)
            return
        else:
            print("The ID's do not match, please try again.")
    else:
        print("This is not your slot, please choose your own slot.")