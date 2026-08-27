import base64
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from django.db.models import Count
from django.shortcuts import render

from .models import Movie


def home(request):
    query = request.GET.get('searchMovie') or request.GET.get('search')
    movies = Movie.objects.all().order_by('title')
    if query:
        movies = movies.filter(title__icontains=query)
    return render(request, 'movie/home.html', {
        'movies': movies,
        'searchTerm': query or '',
    })


def about(request):
    return render(request, 'movie/about.html')


def signup(request):
    email = request.GET.get('email', '')
    return render(request, 'signup.html', {'email': email})


def _chart_to_base64():
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    graphic = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    plt.close()
    return graphic


def statistics_view(request):
    # Películas por año
    year_counts = {}
    for movie in Movie.objects.all():
        key = movie.year if movie.year else 'None'
        year_counts[key] = year_counts.get(key, 0) + 1

    years = list(year_counts.keys())
    year_values = list(year_counts.values())

    plt.figure(figsize=(10, 5))
    plt.bar(range(len(years)), year_values)
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(range(len(years)), years, rotation=90)
    plt.tight_layout()
    year_graphic = _chart_to_base64()

    # Películas por primer género
    genre_counts = {}
    for movie in Movie.objects.all():
        genre = (movie.genre or 'Unknown').split(',')[0].strip()
        genre_counts[genre] = genre_counts.get(genre, 0) + 1

    genres = list(genre_counts.keys())
    genre_values = list(genre_counts.values())

    plt.figure(figsize=(10, 5))
    plt.bar(range(len(genres)), genre_values)
    plt.title('Movies per genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(range(len(genres)), genres, rotation=45, ha='right')
    plt.tight_layout()
    genre_graphic = _chart_to_base64()

    return render(request, 'movie/statistics.html', {
        'year_graphic': year_graphic,
        'genre_graphic': genre_graphic,
    })
