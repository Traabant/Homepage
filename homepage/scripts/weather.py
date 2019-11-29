from weather.models import Weather2, Weather_forcast

class Weather:
    def __init__(self):
        pass

    def get_todays_weather_data_from_db(self):    
        # Gets todays forcast from DB from table weather_weather2.
        # temp is stored in Kelvins in DB, must be converterd to C before returned

        # Pollutin is pulled from DB prom table waether_pollution
        # :return: dict of list of temperaturs for today and tomorow and current pollution data
        

        # gets data for today from DB
       
        temp_from_db = Weather2.objects.all().order_by('-id')[:8]

        
        # turns Queryset object in to list, and then reverse it
        list_from_db_today = []
        for item in temp_from_db:
            list_from_db_today.append(item)
        list_from_db_today.reverse()
        

        # converts temp data in list from K to C
        # uses f string formatting to show only two digits
        for item in list_from_db_today:
            item.weather_today = f'{(float(item.weather_today) - 273.15):.2f}'
            # item = f'{(float(item- 273.15)):.2f}'        
        
        tempDict = {
            f'{list_from_db_today[0].date}': list_from_db_today[0].weather_today,
            f'{list_from_db_today[1].date}': list_from_db_today[1].weather_today,
            f'{list_from_db_today[2].date}': list_from_db_today[2].weather_today,
            f'{list_from_db_today[3].date}': list_from_db_today[3].weather_today,
            f'{list_from_db_today[4].date}': list_from_db_today[4].weather_today,
            f'{list_from_db_today[5].date}': list_from_db_today[5].weather_today,
            f'{list_from_db_today[6].date}': list_from_db_today[6].weather_today,
            f'{list_from_db_today[7].date}': list_from_db_today[7].weather_today,
        }        
        return tempDict

    def get_tomorows_weather_data_from_db(self):    
        # Gets todays forcast from DB from table weather_weather2.
        # temp is stored in Kelvins in DB, must be converterd to C before returned

        # Pollutin is pulled from DB prom table waether_pollution
        # :return: dict of list of temperaturs for today and tomorow and current pollution data
        

        # gets data for today from DB
       
        temp_from_db = Weather_forcast.objects.all().order_by('-id')[:8]

        
        # turns Queryset object in to list, and then reverse it
        list_from_db_today = []
        for item in temp_from_db:
            list_from_db_today.append(item)
        list_from_db_today.reverse()
        

        # converts temp data in list from K to C
        # uses f string formatting to show only two digits
        for item in list_from_db_today:
            item.weather_tomorrow = f'{(float(item.weather_tomorrow) - 273.15):.2f}'
            # item = f'{(float(item- 273.15)):.2f}'        
        
        tempDict = {
            f'{list_from_db_today[0].date_tomorrow}': list_from_db_today[0].weather_tomorrow,
            f'{list_from_db_today[1].date_tomorrow}': list_from_db_today[1].weather_tomorrow,
            f'{list_from_db_today[2].date_tomorrow}': list_from_db_today[2].weather_tomorrow,
            f'{list_from_db_today[3].date_tomorrow}': list_from_db_today[3].weather_tomorrow,
            f'{list_from_db_today[4].date_tomorrow}': list_from_db_today[4].weather_tomorrow,
            f'{list_from_db_today[5].date_tomorrow}': list_from_db_today[5].weather_tomorrow,
            f'{list_from_db_today[6].date_tomorrow}': list_from_db_today[6].weather_tomorrow,
            f'{list_from_db_today[7].date_tomorrow}': list_from_db_today[7].weather_tomorrow,
        }        
        return tempDict
if __name__ == "__main__":
    tempToday = Weather()
    data = tempToday.get_weather_data_from_db(0)
    print(data)
