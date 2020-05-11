from django.shortcuts import render
from .models import Weather2, Consumption, Events, Gallery, Pollution, Weather_forcast, HomeWeather
# from .scripts import consuption, check, radarData

from .scripts import consuption

from scripts import radarData
from scripts import weather as Weather
from scripts.myTime import convert_time_from_UTC
# from scripts import check_events
# from scripts import radarData

from django.http import JsonResponse

from datetime import datetime

def dev(request):

    return render(request, 'weather/tmp.html')


def weather(request):
    context = get_weather_data_from_db()
    if request.method == 'POST':
        check.get_weather()
        context = get_weather_data_from_db()
        return render(request, 'weather/info.html', context)

    return render(request, 'weather/info.html', context)


def consumption(request):
    data_from_db = Consumption.objects.all().last()
    context = {
        'date': data_from_db.date,
        'total_km': data_from_db.total_km,
        'traveled_km': data_from_db.traveled_km,
        'total_fuel':data_from_db.total_fuel,
        'curent_consuption': data_from_db.curent_consuption / 100,
    }

    if request.method == 'POST':
        consuption.main()
        data_from_db = Consumption.objects.all().last()
        context = {
            'date': data_from_db.date,
            'total_km': data_from_db.total_km,
            'traveled_km': data_from_db.traveled_km,
            'total_fuel': data_from_db.total_fuel,
            'curent_consuption': data_from_db.curent_consuption / 100,
        }
        return render(request, 'weather/consumption.html', context)

    return render(request, 'weather/consumption.html', context)


def events(request):
    context= {
        'gallery': Gallery.objects.all(),
        'events': Events.objects.all()
    }

    return render(request, 'weather/events.html', context)

def radarImage(request):
    r = radarData()
    context = r.get_last_x_images()

    return JsonResponse(context)

def dev(request):
    return render(request, 'weather/tmp.html')

##############################################
#            supporting functions            #
##############################################



def get_weather_data_from_db():
    """
    Gets todays forcast from DB from table weather_weather2.
    temp is stored in Kelvins in DB, must be converterd to C before returned

    Pollutin is pulled from DB prom table waether_pollution
    :return: dict of list of temperaturs for today and tomorow and current pollution data
    """

    # gets data for today from DB
    temp_from_db = Weather2.objects.all().order_by('-id')[:8]
    temp_tomorrow_from_db = Weather_forcast.objects.all().order_by('-id')[:8]
    pollution_form_db = Pollution.objects.all().last()

    # turns Queryset object in to list, and then reverse it  
    list_from_db_today = []
    for item in temp_from_db:
        list_from_db_today.append(item)
    list_from_db_today.reverse()

    list_from_db_tomorrow = []
    for item in temp_tomorrow_from_db:
        list_from_db_tomorrow.append(item)
    list_from_db_tomorrow.reverse()

    # cur_temp = HomeWeather.objects.last()
    
    cur_temp = {
        'temperature': HomeWeather.objects.last().temperature,
        'date': (convert_time_from_UTC(HomeWeather.objects.last().date)).strftime("%Y-%m-%d %H:%M"),
    }

    temp_in_K = {
        'temp': list_from_db_today,
        'temp_tomorrow': list_from_db_tomorrow,
        'polution': Weather.Weather().analyze_air_polution(pollution_form_db.pollution_index),
        'pollution_date': pollution_form_db.datetime,
        'polution_index': pollution_form_db.pollution_index,
        'cur_temp':cur_temp,
    }

    # converts temp data in list from K to C
    # uses f string formatting to show only two digits
    for item in temp_in_K['temp']:
        item.weather_today = f'{(float(item.weather_today) - 273.15):.2f}'
    for item in temp_in_K['temp_tomorrow']:
        item.weather_tomorrow = f'{(float(item.weather_tomorrow) - 273.15):.2f}'

    return temp_in_K

# def convert_time_from_UTC(utc_dt):
#     local_tz = pytz.timezone('Europe/Prague')
#     local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
#     return local_dt






