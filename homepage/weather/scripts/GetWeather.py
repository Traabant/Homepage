import json
import requests
import sqlite3
import datetime
from sqlite3 import Error
from django.conf import settings


def convert_K_to_C(temperatureK):
    temperatureC = temperatureK - 273.15
    return temperatureC


def analyze_air_polution(polutin_index):
    if polutin_index == 1:
        return "Velmi dobra"
    elif polutin_index == 2:
        return "dobra"
    elif polutin_index == 3:
        return "uspokojiva"
    elif polutin_index == 4:
        return "vzhovujci"
    elif polutin_index == 5:
        return "spatna"
    elif polutin_index == 6:
        return "velmi spatna"
    else:
        return "Chyba spracovani"


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


def main():
    """
    Downloads focast for current day and stores it in DB
    data is pulled out of the DB in views when needed
    """

    url_forcast = 'http://api.openweathermap.org/data/2.5/forecast?q=ostrava&appid=f38cd70321c379afac4b55fb00a3be7a'

    response = requests.get(url_forcast)
    forcast_data = json.loads(response.text)

    # database = settings.BASE_DIR + "/db.sqlite3"
    fileDir = '/home/Traabant/Homepage/Homepage/homepage'
    database = fileDir + '/db.sqlite3'
    # database = "D:\\SIBA\\Scripty\\Homepage\\homepage\\db.sqlite3"
    conection = create_connection_to_db(database)
    cursor = conection.cursor()

    index = 0
    list_data_today_in_K = []
    while index <= 7:
        data_today_in_K = {
            'date': datetime.datetime.strptime(forcast_data["list"][index]['dt_txt'], '%Y-%m-%d %H:%M:%S'),
            'temp': forcast_data["list"][index]['main']['temp_max'],
        }

        string_to_execute = "INSERT INTO weather_weather2(weather_today, date) VALUES('%.01f','%s')" % (
            data_today_in_K['temp'], data_today_in_K['date'].strftime('%Y-%m-%d %H:%M:%S'))
        list_data_today_in_K.append(data_today_in_K)
        cursor.execute(string_to_execute)
        conection.commit()

        index += 1

    print('weather downloaded')




