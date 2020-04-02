from django.urls import path, include
from . import views

weatherpatterns = [
    path('today', views.todayTemps, name='todayTemps'),
    path('tomorow', views.tomorowTemps, name='tomorowTemps'),
    path('pollution', views.pollution, name='pollution'),
    path('save-home-temps', views.save_temps, name="save-home-temps"),
    path('print', views.print_body, name="print body")
] 

githubPatterns = [
    path('', views.git_repos, name="git_repos" ),
]

urlpatterns = [
    path('', views.index, name='api'),
    path('get-images', views.radarImageNames, name='radarImageNames'),
    path('weather/', include(weatherpatterns)),
    path('github/', include(githubPatterns)),
]

