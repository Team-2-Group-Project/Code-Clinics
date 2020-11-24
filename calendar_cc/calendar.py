import datetime
import statistics
import terminaltables
from terminaltables import AsciiTable
import json
table_data = []

def list_of_times():
    time_list = []
    time = datetime.datetime(year=2020,month=12,day=1,hour=7,minute=30)
    for i in range(20):
        time = time + datetime.timedelta(minutes=30)
        time_list.append(time.strftime('%H:%M'))
        table_data[i+1][0] = time_list[i]
    print(time_list)
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
    for x in range(20):
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
            time_string = x['start']['dateTime'][:-9]
            time_string = time_string[11:]
            index2 = time_list.index(time_string)
            table_data[index2+1][index+1] = creating_slot(x)
        except:
            pass
        count = count + 1

def generate_table(i,dict):
    global table_data
    list_week = creating_list_of_week(i,datetime.date.today())
    temp_list = generate_list_of_empty_strings(i)
    try:
        count,list_of_dates = determine_and_set_table_height(dict,temp_list)
    except:
        return print("1")
    generate_days(i,count,list_week)
    time_list = list_of_times()
    dict = assigning_row_col_num_to_dict(dict,count)
    writing_to_table(dict,count,list_week,list_of_dates,count,time_list)
    table = terminaltables.SingleTable(table_data)
    table.inner_row_border = True
    table.padding_left = 0
    table.padding_right = 0
    print(table.table)
