# Downloads curent data from Google drive
# data are created in Android APP Fueino
# Every new entry in app is synced to GDrive
# stores data in local DB file using SQlite

# URL from Google Drive
# https://drive.google.com/open?id=1_CST2emrtNu1EGvq9h35byyHW1nmKxbu

# MOdified URL for drirect download example:
# https://drive.google.com/uc?export=download&id=FILE_ID
# actual link
# https://drive.google.com/uc?export=download&id=1_CST2emrtNu1EGvq9h35byyHW1nmKxbu

import requests
import sqlite3
from sqlite3 import Error
import datetime
import os
from django.conf import settings
from ..models import Consumption
import matplotlib.pyplot as plt
import numpy as np



def create_connection_to_db(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None


def find_data(list_to_analyze):
    list_to_return = []
    for line in list_to_analyze:
        if is_datetime(line[0]) is True:
            list_to_return.append(line)
    return list_to_return


def is_datetime(string):
    # In Data from Fuelino, only filing gas entries starts with date time
    # Fuelino added time to date log, so i needed to alter test
    import datetime
    try:
        datetime.datetime.strptime(string, "%Y-%m-%d")
        return True
    except:
        try:
            datetime.datetime.strptime(string, "%Y-%m-%d %H:%M")
            return True
        except:
            return False


def url_data_to_list(data_to_split):
    # splist every line in LIST into another LIST
    # returns two dimensional list
    csv_content_splited = []
    csv_content = data_to_split.content
    csv_content = csv_content.decode(encoding='utf-8')
    csv_content = csv_content.splitlines()
    for line in csv_content:
        splited_line = line.split(",")
        csv_content_splited.append(splited_line)
    csv_content_splited = delete_extra_characters(csv_content_splited)
    return csv_content_splited


def delete_extra_characters(data_to_clean):
    # removes extra ". This is needed for next steps
    line_without_extra_chars = []
    list_without_extra_chars = []
    for line in data_to_clean:
        for row in line:
            row = row.replace('"', '')
            line_without_extra_chars.append(row)
        list_without_extra_chars.append(line_without_extra_chars)
        line_without_extra_chars = []
    return list_without_extra_chars


def histroy(list_with_correct_data):
    grafLoacation = '/home/Traabant/Homepage/Homepage/homepage/blog/static/blog/graf.png'
    # grafLoacation = "d:\\SIBA\\Scripty\\Homepage\\homepage\\blog\static\\blog\\graf.png"
    consuption_history = {
        "consuption": [],
        "date": [],
    }
    index = 2
    curent_fuel = float(list_with_correct_data[-1][2])
    while index <= len(list_with_correct_data):
        last_mileage = int(round(float(list_with_correct_data[-index][1])))
        first_mileage = int(round(float(list_with_correct_data[-1][1])))
        total_mileage = last_mileage - first_mileage
        curent_fuel += int(round(float(list_with_correct_data[-index][2])))
        consumption = (curent_fuel / total_mileage) * 100
        consuption_history["consuption"].append(consumption)
        consuption_history["date"].append(list_with_correct_data[-index][0])
        index += 1
    del consuption_history["consuption"][0]   # first entry is off scale
    del consuption_history["date"][0]  # first entry is off scale

    data = {
        "consuption": consuption_history["consuption"],
        "dates": consuption_history["date"],
    }

    return data


def main():
    response = None
    url = 'https://drive.google.com/uc?export=download&id=1_CST2emrtNu1EGvq9h35byyHW1nmKxbu'

    try:
        response = requests.get(url)
    except:
        print("Can not download")

    if response:
        list_with_raw_data = url_data_to_list(response)
        list_with_correct_data = find_data(list_with_raw_data)
        last_mileage = int(round(float(list_with_correct_data[0][1])))
        first_mileage = int(round(float(list_with_correct_data[-1][1])))
        total_mileage = last_mileage - first_mileage
        # print("Total Traveled: %d km" % total_mileage)

        i = 0
        current_fuel = 0
        for item in list_with_correct_data:
            current_fuel += int(round(float(list_with_correct_data[i][2])))
            i += 1
        consumption = (current_fuel / total_mileage) * 100
        date_added = list_with_correct_data[0][0]
        # print("Total fuel : %d liters" % current_fuel)
        # print("consumption : %.2f l*100km-1" % consumption)

        # dump_data_to_consumption_table(last_mileage, total_mileage, current_fuel, consumption)

        data_to_db = Consumption(
            date=date_added, total_km=last_mileage,
            traveled_km=total_mileage, total_fuel=current_fuel, curent_consuption=consumption*100
        )

        history_data = histroy(list_with_correct_data)
        last_entry = Consumption.objects.all().last()

        # checks if its new entry, saves it to DB if it is
        if (history_data['dates'][-1] != last_entry.date):
            data_to_db.save()
        
        return history_data

if __name__ == "__main__":
    main()
