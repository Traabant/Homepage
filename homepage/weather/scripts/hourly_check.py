import requests
import json
import sqlite3
from datetime import datetime, timedelta
from sqlite3 import Error


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


def get_pollution():
    fileDir = '/home/Traabant/Homepage/Homepage/homepage'
    db_file_name = fileDir + '/db.sqlite3'
    db_file_name = 'D:\SIBA\Scripty\Homepage\homepage\db.sqlite3'
    conection = create_connection_to_db(db_file_name)
    cursor = conection.cursor()

    url_json_file = 'http://portal.chmi.cz/files/portal/docs/uoco/web_generator/aqindex_cze.json'
    response = requests.get(url_json_file)
    air_pollution_data = json.loads(response.text)
    index_ostrava_portuba = air_pollution_data['States'][0]['Regions'][13]['Stations'][15]['Ix']
    date_pullution = air_pollution_data['States'][0]['DateFromUTC']
    date_pullution = datetime.strptime(date_pullution, '%Y-%m-%d %H:%M:%S.%f %Z')
    date_pullution = date_pullution + timedelta(hours=2)
    date_pullution = date_pullution.strftime('%Y-%m-%d %H:%M:%S')
    string_to_execute = "INSERT INTO weather_pollution(datetime, pollution_index) VALUES('%s', '%d')" % (date_pullution, index_ostrava_portuba)
    cursor.execute(string_to_execute)
    conection.commit()
    print(f'Aktualni index {index_ostrava_portuba} z {date_pullution} stazeno {datetime.now()}')

get_pollution()

