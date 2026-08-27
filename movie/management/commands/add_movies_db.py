import csv
import re
import unicodedata
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from PIL import Image, ImageDraw, ImageFont

from movie.models import Movie


def slugify_title(value):
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii').lower()
    return re.sub(r'[^a-z0-9]+', '-', value).strip('-')[:70] or 'movie'


def create_movie_cover(path, title, genre, year):
    """Crea una portada local para que todas las películas tengan imagen."""
    path.parent.mkdir(parents=True, exist_ok=True)
    width, height = 600, 900
    image = Image.new('RGB', (width, height), '#16213e')
    draw = ImageDraw.Draw(image)

    # Fondo cinematográfico sencillo y sin depender de imágenes externas.
    draw.rectangle((0, 0, width, 170), fill='#111827')
    for x in range(-30, width + 50, 85):
        draw.rounded_rectangle((x, 48, x + 55, 125), radius=8, outline='white', width=3)
    draw.ellipse((120, 230, 480, 590), outline='white', width=9)
    for cx, cy in ((300, 325), (215, 410), (385, 410), (300, 495)):
        draw.ellipse((cx - 36, cy - 36, cx + 36, cy + 36), fill='#e5e7eb')
    draw.ellipse((270, 380, 330, 440), fill='#111827')
    draw.rounded_rectangle((45, 615, 555, 845), radius=25, fill='#111827', outline='white', width=2)

    # ImageFont.load_default() evita depender de fuentes instaladas en el equipo.
    title_font = ImageFont.load_default(size=34)
    meta_font = ImageFont.load_default(size=22)

    words = title.split()
    lines, current = [], ''
    for word in words:
        candidate = f'{current} {word}'.strip()
        if draw.textbbox((0, 0), candidate, font=title_font)[2] <= 440:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)

    y = 650
    for line in lines[:3]:
        box = draw.textbbox((0, 0), line, font=title_font)
        draw.text(((width - (box[2] - box[0])) / 2, y), line, font=title_font, fill='white')
        y += 46

    meta = f"{year or '—'} • {(genre or 'Sin género').split(',')[0]}"
    box = draw.textbbox((0, 0), meta, font=meta_font)
    draw.text(((width - (box[2] - box[0])) / 2, 805), meta, font=meta_font, fill='#fbbf24')
    image.save(path, 'JPEG', quality=88)


class Command(BaseCommand):
    help = 'Carga las películas desde movies_initial.csv y crea una portada para cada una.'

    def handle(self, *args, **options):
        csv_path = Path(__file__).with_name('movies_initial.csv')
        image_dir = Path(settings.MEDIA_ROOT) / 'movie' / 'images'

        Movie.objects.all().delete()
        movies = []
        with csv_path.open(encoding='utf-8-sig', newline='') as file:
            for index, row in enumerate(csv.DictReader(file), start=1):
                title = row['title'].strip()
                genre = row['genre'].strip()
                year = int(row['year']) if row['year'].strip() else None
                filename = f'{index:03d}-{slugify_title(title)}.jpg'
                create_movie_cover(image_dir / filename, title, genre, year)

                movies.append(Movie(
                    title=title,
                    genre=genre,
                    year=year,
                    description=row['description'].strip(),
                    image=f'movie/images/{filename}',
                ))

        Movie.objects.bulk_create(movies)
        self.stdout.write(self.style.SUCCESS(
            f'{len(movies)} películas cargadas correctamente, cada una con su portada.'
        ))
