from django.shortcuts import render
from .models import Weather2

# Create your views here.


def weather(request):
    # temp is stored in Kelins in DB, must be converterd to C before send to template
    temp_in_K = {
        'temp': Weather2.objects.get().weather_today
    }
    Data = {
        'tempC': float(temp_in_K['temp']) - 273.15,
        'date': Weather2.objects.get().date
    }
    #print(temp_in_C['temp'])
    return render(request, 'weather/info.html', Data, )
