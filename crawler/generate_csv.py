# -*- coding: utf-8 -*-

import pandas as pd
import json
from os import listdir
from copy import copy

JSON_PATH = './ksou/data/json/'
df = None
is_first_time = True
count = 0
CSV_PATH = './csv/'
CSV_NAME = 'ksou_parsed_from_json.csv'
cols = [    "id","address","nearbySchoolNum","houseType","soldPrice",
    "lastSoldPrice",
    "rentPrice",
    "bedroom",
    "bathroom",
    "carspace",
    "soldTimeYear", "soldTimeMonth",
    "lastSoldTimeYear",
    "lastSoldTimeMonth",
    "rentTimeYear",
    "rentTimeMonth",
    "landSize",
    "buildingSize",
    "buildYear",
    "distanceToCBD",
    "distanceToStation"]

def month_to_num(string):
    m = {
        'jan': 1,
        'feb': 2,
        'mar': 3,
        'apr':4,
         'may':5,
         'jun':6,
         'jul':7,
         'aug':8,
         'sep':9,
         'oct':10,
         'nov':11,
         'dec':12
        }
    s = string.strip()[:3].lower()
    try:
        out = m[s]
        return out
    except:
        raise ValueError('Not a month')

def read_json(file_name):
    with open(JSON_PATH + file_name,'r') as f:
        return json.load(f)

def replace_with_null(json_content):
    for key in json_content:
        if json_content[key] == '-1':
            json_content[key] = ''
            
def parse_time(string):
    if string:
        timearr = string.split(' ')
        return timearr[1], month_to_num(timearr[0])
    else:
        return '',''

def parse_all_time(cur_data):
    soldTime = cur_data.pop('soldTime', None)
    lastSoldTime = cur_data.pop('lastSoldTime', None)
    rentTime = cur_data.pop('rentTime', None)
    soldTimeYear, soldTimeMonth = parse_time(soldTime)
    lastSoldTimeYear, lastSoldTimeMonth = parse_time(lastSoldTime)
    rentTimeYear, rentTimeMonth = parse_time(rentTime)
    cur_data['soldTimeYear'] = soldTimeYear
    cur_data['soldTimeMonth'] = soldTimeMonth
    cur_data['lastSoldTimeYear'] = lastSoldTimeYear
    cur_data['lastSoldTimeMonth'] = lastSoldTimeMonth
    cur_data['rentTimeYear'] = rentTimeYear
    cur_data['rentTimeMonth'] = rentTimeMonth

def create_data_from_last_sold(cur_data):
    lastSoldPrice = cur_data.pop('lastSoldPrice', None)
    lastSoldTime = cur_data.pop('lastSoldTime', None)
    if not lastSoldPrice:
        return None
    last_sold_data = copy(cur_data)
    last_sold_data['soldPrice'] = lastSoldPrice
    last_sold_data['soldTime'] = lastSoldTime
    return last_sold_data


def save_df_file():
    df.to_csv(CSV_PATH + CSV_NAME, index=False)
         
         
def save_json_to_df(file_name):
    global df, is_first_time, count
    count += 1
    cur_data = read_json(file_name)
    replace_with_null(cur_data)
    parse_all_time(cur_data)
#    last_sold_data = create_data_from_last_sold(cur_data)
    cur_df = pd.DataFrame([cur_data], columns = cols)
    if is_first_time:
        print(is_first_time)
        df = cur_df
        is_first_time = False
    else:
        df = pd.concat([df, cur_df], ignore_index=True)
    if count % 1000 == 100:
        df = df.sort(columns = 'id')
        save_df_file()


def main():
    global df
    json_files = listdir(JSON_PATH)
#    save_json_to_df('2.json')
    for file_name in json_files:
        print('Parsing:', file_name)
        save_json_to_df(file_name)


if __name__ == "__main__":
    main()