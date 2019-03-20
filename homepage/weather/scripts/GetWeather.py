import json
import requests
import sqlite3
import datetime
from sqlite3 import Error


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



# Download JSON from CHMI
url_json_file = 'http://portal.chmi.cz/files/portal/docs/uoco/web_generator/aqindex_cze.json'
response = requests.get(url_json_file)
air_pollution_data = json.loads(response.text)

# offline version for debuging
# weather_input_file_path = "d:\\SIBA\\Scripty\\Projekt\\aqindex_cze.json"
# air_pollution_data = open(weather_input_file_path, "r", encoding="utf-8")
# json_data = json.load(air_pollution_data)

index_ostrava_portuba = air_pollution_data['States'][0]['Regions'][13]['Stations'][15]['Ix']
print("Kvalita ovzdusi je %s" % (analyze_air_polution(index_ostrava_portuba)))

# TODO: save index_ostrava_poruba to DB
# DONE: Download todays weather update
# TODO: make homepage shownig this data


# odkaz pro stazeni aktualni informace o pocasi
# muj Api klic f38cd70321c379afac4b55fb00a3be7a
# http://api.openweathermap.org/data/2.5/weather?q=ostrava&appid=f38cd70321c379afac4b55fb00a3be7a
# predpoved na tri dny
# http://api.openweathermap.org/data/2.5/forecast?q=ostrava&appid=f38cd70321c379afac4b55fb00a3be7a

url_forcast = 'http://api.openweathermap.org/data/2.5/forecast?q=ostrava&appid=f38cd70321c379afac4b55fb00a3be7a'

response = requests.get(url_forcast)
forcast_data = json.loads(response.text)
temperature_today_in_K = forcast_data["list"][0]['main']['temp_max']
temperature_today_in_C = convert_K_to_C(temperature_today_in_K)
print("Dnesni teplota bude %.2f C" % temperature_today_in_C)

temperature_tomorow_in_K = forcast_data["list"][8]['main']['temp_max']
temperature_tomorow_in_C = convert_K_to_C(temperature_tomorow_in_K)
print("Zitrejsi teplota bude %.2f C" % temperature_tomorow_in_C)

database = "D:\\SIBA\\Scripty\\Homepage\\homepage\\db.sqlite3"
today = datetime.datetime.today().strftime("%Y-%m-%d")

conection = create_connection_to_db(database)
cursor = conection.cursor()
last_row_id = cursor.lastrowid
string_to_execute = "INSERT INTO weather_weather2(weather_today, date) VALUES('%.01f','%s')" %(temperature_today_in_K, today)
cursor.execute(string_to_execute)

conection.commit()


print('Done')
