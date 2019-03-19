from django.shortcuts import render
from .models import Post


def home(request):
    context = {
        # Retur data from DB
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


def about(request):
    return render(request, 'blog/about.html')


def events(reqeust):
    return render(reqeust, 'blog/events.html')


# Create your views here.
