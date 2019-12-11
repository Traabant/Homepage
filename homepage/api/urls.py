from django.urls import path, include
from . import views

weatherpatterns = [
    path('today', views.todayTemps, name='todayTemps'),
    path('tomorow', views.tomorowTemps, name='tomorowTemps'),
    path('pollution', views.pollution, name='pollution'),
] 

urlpatterns = [
    path('', views.index, name='api'),
    path('get-images', views.radarImageNames, name='radarImageNames'),
    path('weather/', include(weatherpatterns)),

]

