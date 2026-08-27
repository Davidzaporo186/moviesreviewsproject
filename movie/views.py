import base64
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from django.db.models import Count
from django.shortcuts import render

from .models import Movie


def home(request):
    movies = Movie.objects.all().order_by('title')
    return render(request, 'movie/home.html', {
        'movies': movies,
        'searchTerm': '',
    })


def search_movies(request):
    """Busca películas por título usando una coincidencia parcial."""
    query = (request.GET.get('searchMovie') or request.GET.get('search') or '').strip()
    movies = Movie.objects.all().order_by('title')
    if query:
        movies = movies.filter(title__icontains=query)
    return render(request, 'movie/home.html', {
        'movies': movies,
        'searchTerm': query,
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
    # Películas por año: se ordenan cronológicamente para que la gráfica sea legible.
    year_counts = {}
    for movie in Movie.objects.exclude(year__isnull=True):
        year_counts[movie.year] = year_counts.get(movie.year, 0) + 1

    years = sorted(year_counts)
    year_values = [year_counts[year] for year in years]

    plt.figure(figsize=(12, 5))
    plt.bar(years, year_values)
    plt.title('Películas por año')
    plt.xlabel('Año')
    plt.ylabel('Cantidad de películas')
    plt.xticks(rotation=90, fontsize=7)
    plt.grid(axis='y', alpha=0.2)
    plt.tight_layout()
    year_graphic = _chart_to_base64()

    # Películas por género: una película suma en cada género que tenga en el dataset.
    genre_counts = {}
    for movie in Movie.objects.all():
        genres_for_movie = [g.strip() for g in (movie.genre or 'Unknown').split(',') if g.strip()]
        for genre in genres_for_movie or ['Unknown']:
            genre_counts[genre] = genre_counts.get(genre, 0) + 1

    genres = sorted(genre_counts, key=genre_counts.get, reverse=True)
    genre_values = [genre_counts[genre] for genre in genres]

    plt.figure(figsize=(12, 5))
    plt.bar(genres, genre_values)
    plt.title('Películas por género')
    plt.xlabel('Género')
    plt.ylabel('Cantidad de películas')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.2)
    plt.tight_layout()
    genre_graphic = _chart_to_base64()

    return render(request, 'movie/statistics.html', {
        'year_graphic': year_graphic,
        'genre_graphic': genre_graphic,
    })
