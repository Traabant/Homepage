from django.shortcuts import render
from .models import Weather2
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
    #print("Kvalita ovzdusi je %s" % (analyze_air_polution(index_ostrava_portuba)))

    temp_in_K = {
        'temp': Weather2.objects.get().weather_today
    }
    Data = {
        'tempC': float(temp_in_K['temp']) - 273.15,
        'date': Weather2.objects.get().date,
        'polution': analyze_air_polution(index_ostrava_portuba)
    }

    return render(request, 'weather/info.html', Data)
