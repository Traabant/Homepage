from django.shortcuts import render
from .models import Weather2, Consumption, Events, Gallery
from .scripts import GetWeather, consuption, check
import json
import requests

# Views


def weather(request):
    data = get_weather_data_from_db()
    if request.method == 'POST':
        GetWeather.main()
        data = get_weather_data_from_db()
        return render(request, 'weather/info.html', data)

    return render(request, 'weather/info.html', data)


def consumption(request):
    data_from_db = Consumption.objects.all().last()
    data = {
        'date': data_from_db.date,
        'total_km': data_from_db.total_km,
        'traveled_km': data_from_db.traveled_km,
        'total_fuel':data_from_db.total_fuel,
        'curent_consuption': data_from_db.curent_consuption / 100,
    }

    if request.method == 'POST':
        consuption.main()
        data_from_db = Consumption.objects.all().last()
        data = {
            'date': data_from_db.date,
            'total_km': data_from_db.total_km,
            'traveled_km': data_from_db.traveled_km,
            'total_fuel': data_from_db.total_fuel,
            'curent_consuption': data_from_db.curent_consuption / 100,
        }
        return render(request, 'weather/consumption.html', data)

    return render(request, 'weather/consumption.html', data)


def events(request):
    data= {
        'gallery': Gallery.objects.all(),
        'events': Events.objects.all()
    }

    if request.method == 'POST':
        check.mainloop()
        return render(request, 'weather/events.html')

    return render(request, 'weather/events.html', data)

##############################################
#            supporting functions            #
##############################################



def get_weather_data_from_db():
    """
    temp is stored in Kelins in DB, must be converterd to C before returned
    downloads JSON from CHMI Website
    parsing it than selecting data for O-poruba only
    :return: dict of list of temperaturs and current pollution data
    """
    #
    url_json_file = 'http://portal.chmi.cz/files/portal/docs/uoco/web_generator/aqindex_cze.json'
    response = requests.get(url_json_file)
    air_pollution_data = json.loads(response.text)
    index_ostrava_portuba = air_pollution_data['States'][0]['Regions'][13]['Stations'][15]['Ix']

    # gets data from DB
    data_from_db = Weather2.objects.all().order_by('-id')[:6]

    # turns Queryset object in to list, and then reverse it
    list_from_db =[]
    for item in data_from_db:
        list_from_db.append(item)
    list_from_db.reverse()

    temp_in_K = {
        'temp': list_from_db,
        'polution': GetWeather.analyze_air_polution(index_ostrava_portuba),
        'polution_index': index_ostrava_portuba,
    }

    # converts temp data in list from K to C
    # uses f string formatting to show only two digits
    for item in temp_in_K['temp']:
        item.weather_today = f'{(float(item.weather_today) - 273.15):.2f}'
    return temp_in_K
