from django.shortcuts import render

from django.http import JsonResponse
from scripts import radarData, weather

# Create your views here.

def index(request):

    return render(request, 'blog/api.html')


def radarImageNames(request):
    r = radarData.radarData()
    context = r.get_last_x_images()

    return JsonResponse(context)

def todayTemps(request):
    w = weather.Weather()
    context = w.get_weather_data_from_db(0)
    return JsonResponse(context)

def tomorowTemps(request):
    w = weather.Weather()    
    context = w.get_weather_data_from_db(1)
    return JsonResponse(context)

def pollution(request):
    w = weather.Weather()
    context = w.polution()
    return JsonResponse(context)