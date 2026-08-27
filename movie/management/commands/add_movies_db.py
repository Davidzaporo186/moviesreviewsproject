import csv
from pathlib import Path
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = 'Carga las películas desde movies_initial.csv'

    def handle(self, *args, **options):
        csv_path = Path(__file__).with_name('movies_initial.csv')
        Movie.objects.all().delete()
        movies = []
        with csv_path.open(encoding='utf-8-sig', newline='') as file:
            for row in csv.DictReader(file):
                movies.append(Movie(
                    title=row['title'].strip(),
                    genre=row['genre'].strip(),
                    year=int(row['year']) if row['year'].strip() else None,
                    description=row['description'].strip(),
                ))
        Movie.objects.bulk_create(movies)
        self.stdout.write(self.style.SUCCESS(f'{len(movies)} películas cargadas correctamente.'))
