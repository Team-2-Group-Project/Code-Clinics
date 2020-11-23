import datetime
import statistics
import terminaltables
from terminaltables import AsciiTable
import json
table_data = []
full_time_list = [['08:00'], ['08:30', '09:00', '09:30'], ['10:00', '10:30', '11:00'], ['11:30', '12:00', '12:30'], ['13:00', '13:30', '14:00'], ['14:30', '15:00', '15:30'], ['16:00', '16:30', '17:00'], ['17:30']]

def find_time(x):
    count = 1
    time_string = x['start']['dateTime'][:-9]
    time_string = time_string[11:]
    for y in full_time_list:
        try:
            index = y.index(time_string)
            return count
        except:
            pass
        count = count + 1
    return None

def list_of_times():
    time_list = []
    time = datetime.datetime(year=2020,month=12,day=1,hour=7,minute=0)
    time_list.append('08:00')
    table_data[1][0] = time_list[0]
    for i in range(6):
        time = time + datetime.timedelta(minutes=90)
        time_list.append(time.strftime('%H:%M'))
        table_data[i+2][0] = time_list[i+1]
    time_list.append('17:30')
    table_data[8][0] = time_list[7]
    return time_list


def creating_slot(dict):
    try:
        string = 'Title: ' + dict['summary']
    except:
        string = 'Title: None'
    string = string + '\nCreator: ' + dict['creator']['email']
    time_string = dict['start']['dateTime'][:-9]
    time_string = time_string[11:]
    return (string + '\nTime: ' + time_string)

def creating_list_of_week(i,today_date):
    list_week = []
    for i in range(i):
        list_week.append(today_date + datetime.timedelta(days=i))
        list_week[i] = list_week[i].strftime('%Y-%m-%d')
    return list_week

def generate_days(i,r,list_week):
    global table_data
    table_data[0].append('')
    for x in range(i):
        table_data[0].append(list_week[x])

def generate_list_of_empty_strings(i):
    temp_list = []
    for x in range(i):
        temp_list.append('')
    return temp_list

def determine_and_set_table_height(dict,temp_list):
    global table_data
    list_of_dates = []
    for x in dict:
        list_of_dates.append(x['start']['dateTime'][:-15])
    most_common = statistics.mode(list_of_dates)
    table_data.append([])
    count = 0
    # for x in list_of_dates:
    #     if x == most_common:
    #         count = count + 1
    #         table_data.append(temp_list.copy())
    for x in range(8):
        table_data.append(temp_list.copy())
    return count,list_of_dates


def assigning_row_col_num_to_dict(dict,max):
    count = 0
    for x in dict:
        count = count + 1
        x['row_num'] = count
        if count == max:
            count = 0
    return dict

def writing_to_table(dict,rows, list_week, list_of_dates,max,time_list):
    global table_data
    count = 1
    for x in dict:
        try:
            index = list_week.index(x['start']['dateTime'][:-15])
            # time_string = x['start']['dateTime'][:-9]
            # time_string = time_string[11:]
            index2 = find_time(x)
            table_data[index2][index+1] = '    ' + 'X'
            # '    ' + u'\N{check mark}'
        except:
            pass
        count = count + 1

# def filling_up_table():


def generate_table(i,dict):
    global table_data
    list_week = creating_list_of_week(i,datetime.date.today())
    temp_list = generate_list_of_empty_strings(i)
    count,list_of_dates = determine_and_set_table_height(dict,temp_list)
    generate_days(i,count,list_week)
    time_list = list_of_times()
    dict = assigning_row_col_num_to_dict(dict,count)
    writing_to_table(dict,count,list_week,list_of_dates,count,time_list)
    

def print_table(i,events):
    generate_table(i,events)
    table = terminaltables.SingleTable(table_data)
    table.inner_row_border = True
    table.padding_left = 0
    table.padding_right = 0
    print(table.table)