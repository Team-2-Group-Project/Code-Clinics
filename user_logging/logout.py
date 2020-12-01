import json, os

def logout():
    with open('.user_info.json', 'r+') as f:
        data = json.load(f)
    data['user'] = ''
    data['role'] = ''
    data['expire'] = ''
    with open('.user_info.json', 'w+') as f:
        json.dump(data, f)
    try:
        os.remove('token.pickle')
    except:
        pass 