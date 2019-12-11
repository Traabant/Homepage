from weather.models import Weather2, Weather_forcast, Pollution
import datetime


class Weather:
    
    def get_weather_data_from_db(self, dayOffset):    
        """
        parm: dayOffset - determines from what table to pull data
        return: dict{
          string with datetime ("%Y-%m-%d %H:%M:%S): float with temp in C
        }
        Gets todays forcast from DB from table weather_weather2.
        temp is stored in Kelvins in DB, must be converterd to C before returned
       
        gets data for today from DB
        Off set 0 is for today table
        Offset 1 is for tomorow
        """

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
    
    def analyze_air_polution(self, polutin_index):    
        """
        converts Int index to String
        :param polutin_index: index from CHMI json data
        :return: string corresponding to the index
        """
        
        if polutin_index == 1:
            return "Excelenty"
        elif polutin_index == 2:
            return "Verry good"
        elif polutin_index == 3:
            return "Good"
        elif polutin_index == 4:
            return "Suitable"
        elif polutin_index == 5:
            return "Bad"
        elif polutin_index == 6:
            return "Verry bad"
        else:
            return "error"

    def polution(self):
        """
        gets last entry in Pollution table
        returns dict {
        string,
        string with datetime "%Y-%m-%d %H:%M",
        intiget
        }
        """
        pollution_form_db = Pollution.objects.all().last()
        data = {
            'polution': self.analyze_air_polution(pollution_form_db.pollution_index),
            'pollution_date': datetime.datetime.strftime(pollution_form_db.datetime, "%Y-%m-%d %H:%M"),
            'polution_index': pollution_form_db.pollution_index,
        }
        return data


if __name__ == "__main__":
    tempToday = Weather()
    data = tempToday.get_weather_data_from_db(0)
    print(data)
