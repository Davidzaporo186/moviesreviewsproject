from django.shortcuts import render
from .models import Movie


def home(request):
    query = request.GET.get('search')

    if query:
        movies = Movie.objects.filter(title__icontains=query)
    else:
        movies = Movie.objects.all()

    return render(request, 'movie/home.html', {
        'movies': movies
    })


def about(request):
    return render(request, 'movie/about.html')