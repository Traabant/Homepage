from django.shortcuts import render

from django.http import JsonResponse
from scripts import radarData, weather

from github.models import repos, authors
from weather.models import HomeWeather

from django.views.decorators.csrf import csrf_exempt


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
    

def git_repos(request):
    
    data_from_db = repos.objects.all()
    context = []
    for repo in data_from_db:
        owener = authors.objects.get(git_id=repo.owner_id)
        data = {
            "id": repo.git_id,
            'name': repo.name,
            'html': repo.html,
            'git_html': repo.git_html,
            'owner': owener.login,
            'description': repo.description,
        }
        context.append(data)    
        response = JsonResponse(context, safe=False)

        response["Access-Control-Allow-Origin"] = "https://traabant.github.io"
        response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
        response["Access-Control-Allow-Credentials"] = "true"
    
    return response

@csrf_exempt
def print_body(request):
    r = radarData.radarData()
    context = r.get_last_x_images()

    print(request.POST['message'])

    return JsonResponse(context)


@csrf_exempt
def save_temps(request):
    temp = request.POST['temperature']
    pressure = request.POST['pressure']
    room = request.POST['room']

    data = HomeWeather(temperature=temp, pressure = pressure, room= room)
    data.save()

    r = radarData.radarData()
    context = r.get_last_x_images()
    return JsonResponse(context)
