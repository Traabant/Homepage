from weather.models import Weather2, Weather_forcast


class Weather:
    def __init__(self):
        pass

    def get_weather_data_from_db(self, dayOffset):    
        # parm: dayOffset - determines from what table to pull data
        # return: dict{
        #   string with datetime ("%Y-%m-%d %H:%M:%S): float with temp in C
        # }
        # Gets todays forcast from DB from table weather_weather2.
        # temp is stored in Kelvins in DB, must be converterd to C before returned
       
        # gets data for today from DB
        # Off set 0 is for today table
        # Offset 1 is for tomorow
        # 

        if (dayOffset == 0):
            temp_from_db = Weather2.objects.all().order_by('-id')[:8]
        elif(dayOffset == 1):
            temp_from_db = Weather_forcast.objects.all().order_by('-id')[:8]
  
        else:
            return {'er': 'data not found'}
        
        # turns Queryset object in to list, and then reverse it
        list_from_db = []
        for item in temp_from_db:
            list_from_db.append(item)
        list_from_db.reverse()        

        # converts temp data in list from K to C
        # uses f string formatting to show only two digits             
        # Populates dictionary to return
        tempDict = {}
        if (dayOffset == 0):
            for i, item in enumerate(list_from_db):
                item.weather_today = f'{(float(item.weather_today) - 273.15):.2f}'
                tempDict[list_from_db[i].date] =  float(list_from_db[i].weather_today)

        elif (dayOffset == 1):
            for i, item in enumerate(list_from_db):
                item.weather_tomorrow = f'{(float(item.weather_tomorrow) - 273.15):.2f}'
                tempDict[list_from_db[i].date_tomorrow] =  float(list_from_db[i].weather_tomorrow)
        
        return tempDict

if __name__ == "__main__":
    tempToday = Weather()
    data = tempToday.get_weather_data_from_db(0)
    print(data)
