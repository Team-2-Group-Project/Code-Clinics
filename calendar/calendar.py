import datetime
import statistics
import terminaltables
from terminaltables import AsciiTable
import json
table_data = []

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
    for x in list_of_dates:
        if x == most_common:
            count = count + 1
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

def writing_to_table(dict,rows, list_week, list_of_dates,max):
    global table_data
    count = 1
    for x in dict:
        try:
            index = list_week.index(x['start']['dateTime'][:-15])
            table_data[x['row_num']][index] = creating_slot(x)
        except:
            pass
        count = count + 1

def generate_table(i,dict):
    global table_data
    list_week = creating_list_of_week(i,datetime.date.today())
    temp_list = generate_list_of_empty_strings(i)
    count,list_of_dates = determine_and_set_table_height(dict,temp_list)
    generate_days(i,count,list_week)
    dict = assigning_row_col_num_to_dict(dict,count)
    writing_to_table(dict,count,list_week,list_of_dates,count)
    table = terminaltables.SingleTable(table_data)
    table.inner_row_border = True
    table.padding_left = 0
    table.padding_right = 0
    print(table.table)
