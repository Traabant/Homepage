from django.shortcuts import render

from django.http import JsonResponse
from scripts import radarData

# Create your views here.
def radarImage(request):
    r = radarData.radarData()
    data = r.get_last_x_images()

    return JsonResponse(data)