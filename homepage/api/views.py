from django.shortcuts import render

from django.http import JsonResponse
from scripts import radarData, weather

# Create your views here.

def index(request):

    return render(request, 'blog/api.html')


def radarImageNames(request):
    r = radarData.radarData()
    data = r.get_last_x_images()

    return JsonResponse(data)

def todayTemps(request):
    tempToday = weather.Weather()
    data = tempToday.get_weather_data_from_db(0)
    return JsonResponse(data)

def tomorowTemps(request):
    tempToday = weather.Weather()    
    data = tempToday.get_weather_data_from_db(1)
    return JsonResponse(data)