from django.urls import path
from . import views

urlpatterns = [
    path('get-images', views.radarImage, name='radarImage'),

]
