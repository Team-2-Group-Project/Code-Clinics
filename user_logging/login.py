import json, datetime, sys, os
USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../'))
# print(USER_PATHS)
sys.path.insert(0, USER_PATHS + "/")
from api_calls import serives_maker, event_maker


def user_name_func():
    '''
    Asking for the username, therfore it can connect to their email address
    '''
    user_name = input((f"Enter your WeThinkCode Student User_Name: "))
    return user_name


def which_role(user_name):
    possible_roles = ['c','p','clinician', 'patient']
    role = input(f"Hello {user_name}, are you a Clinician (C) or a Patient (P)? ")
    while role.lower() not in possible_roles:
        role = input(f"Please state if you are a Clinician (C) or a Patient (P)? ")
    # return role.lower()
    with open('.user_info.json') as f:
        data = json.load(f)
    if role == data['role']:
        return role.lower()
    else:
        data['role'] = role.lower()
        with open('.user_info.json', 'w+') as f:
            json.dump(data, f)
        return role.lower()


def log_in_checker():
    user_name = ''
    with open(USER_PATHS + '/.user_info.json', 'r+') as f:
        data = json.load(f)
    if data['expire'] == '':
        data['expire'] = datetime.datetime.now() + datetime.timedelta(hours=8)
        data['expire'] = data['expire'].strftime("%Y/%m/%d, %H:%M:%S")
        with open(USER_PATHS + '/.user_info.json', 'w+') as f:
            json.dump(data, f)
    elif datetime.datetime.strptime(data['expire'],'%Y/%m/%d, %H:%M:%S') > datetime.datetime.now():
        return data['user'],data['role']
    else:
        data['user'] = ''
        data['role'] = ''
        data['expire'] = datetime.datetime.now() + datetime.timedelta(hours=8)
        data['expire'] = data['expire'].strftime("%Y/%m/%d, %H:%M:%S")
        with open(USER_PATHS + '/.user_info.json', 'w+') as f:
            json.dump(data, f)
    if data['user'] == '':
        user_name = user_name_func()
        serives_maker.creating_service()
        data['user'] = user_name
        with open(USER_PATHS + '/.user_info.json', 'w+') as f:
            json.dump(data, f)
    # else:
    #     os.remove('token.pickle')
    #     creating_service()
    #     # data['user'] = user_name
    #     with open('.user_info.json', 'w+') as f:
    #         json.dump(data, f)
    #     return
    # if data['role'] == '':
    #     role = which_role(data['user'])
    # else:
    #     role = data['role']
    return data['user']
