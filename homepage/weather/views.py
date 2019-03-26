from django.shortcuts import render
from .models import Weather2, Consumption
from .scripts import GetWeather, consuption
import json
import requests

# Create your views here.

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


def weather(request):
    # temp is stored in Kelins in DB, must be converterd to C before send to template

    url_json_file = 'http://portal.chmi.cz/files/portal/docs/uoco/web_generator/aqindex_cze.json'
    response = requests.get(url_json_file)
    air_pollution_data = json.loads(response.text)
    index_ostrava_portuba = air_pollution_data['States'][0]['Regions'][13]['Stations'][15]['Ix']
    # print("Kvalita ovzdusi je %s" % (analyze_air_polution(index_ostrava_portuba)))

    GetWeather.main()
    data_from_db = Weather2.objects.all().last()
    temp_in_K = {
        'temp': data_from_db.weather_today
    }
    Data = {
        'tempC': float(temp_in_K['temp']) - 273.15,
        'date': data_from_db.date,
        'polution': analyze_air_polution(index_ostrava_portuba)
    }
    # Data = {
    #     'tempC': 1,
    #     'date': 2,
    #     'polution': 3,
    # }

    return render(request, 'weather/info.html', Data)


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
        return render(request, 'weather/consumption.html', data)

    data_from_db = Consumption.objects.all().last()

    return render(request, 'weather/consumption.html', data)
