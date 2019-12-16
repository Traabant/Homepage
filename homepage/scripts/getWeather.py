from scripts.credentials import Credentials
from scripts.DbOperations import DbOperations

import requests
import json
import datetime

class GetWeather():
    """
    class for fething data from web
    Its not ment to be run in django, so no models here, 
    that's why its seperate from weather class
    this script should be run by cron, periodicly
    """

    def get_pollution(self):
        """
        dwonloads Json data about pollution, than i gets parsed for just Ostrava
        Parsed data is stored in DB
        should be run periodically every hour
        """

        db = DbOperations(Credentials().db_file_name)

        url_json_file = 'http://portal.chmi.cz/files/portal/docs/uoco/web_generator/aqindex_cze.json'
        response = requests.get(url_json_file)
        air_pollution_data = json.loads(response.text)
        index_ostrava_portuba = air_pollution_data['States'][0]['Regions'][13]['Stations'][15]['Ix']
        date_pullution = air_pollution_data['States'][0]['DateFromUTC']
        date_pullution = datetime.datetime.strptime(date_pullution, '%Y-%m-%d %H:%M:%S.%f %Z')
        date_pullution = date_pullution + datetime.timedelta(hours=2)
        date_pullution = date_pullution.strftime('%Y-%m-%d %H:%M:%S')
        if index_ostrava_portuba != 0:
            db.dump_data_pollution_table(date_pullution, index_ostrava_portuba)
            print("data saved in DB")
        print(f'Aktualni index {index_ostrava_portuba} z {date_pullution} stazeno {datetime.datetime.now()}')


    def get_weather(self):
        """
        Downloads focast for current and next day, then stores it in DB
        data is pulled out of the DB in views when needed
        """

        url_forcast = 'http://api.openweathermap.org/data/2.5/forecast?q=ostrava&appid=f38cd70321c379afac4b55fb00a3be7a'

        response = requests.get(url_forcast)
        forcast_data = json.loads(response.text)

        db = DbOperations(Credentials().db_file_name)
        index = 0
        while index <= 7:
            data_today_in_kelvin = {
                'date': datetime.datetime.strptime(forcast_data["list"][index]['dt_txt'], '%Y-%m-%d %H:%M:%S'),
                'temp': forcast_data["list"][index]['main']['temp_max'],
            }
            db.dump_data_weather_table(data_today_in_kelvin['temp'],
                                    data_today_in_kelvin['date'].strftime('%Y-%m-%d %H:%M:%S'))
            index += 1
        index = 8
        while index <= 15:
            data_tomorrow_in_kelvin = {
                'date_added': datetime.datetime.now(),
                'date_tomorrow': datetime.datetime.strptime(forcast_data["list"][index]['dt_txt'], '%Y-%m-%d %H:%M:%S') ,
                'temp': forcast_data["list"][index]['main']['temp_max'],
            }
            index += 1
            db.dump_data_weather_forcast_table(data_tomorrow_in_kelvin['temp'],
                                            data_tomorrow_in_kelvin['date_tomorrow'],
                                            data_tomorrow_in_kelvin['date_added']
                                            )

        print('weather downloaded')
