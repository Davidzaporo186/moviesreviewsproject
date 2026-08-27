import csv
from datetime import datetime
from pathlib import Path
from django.core.management.base import BaseCommand
from news.models import News

class Command(BaseCommand):
    help = 'Carga cinco noticias desde Fake.csv'

    def handle(self, *args, **options):
        csv_path = Path(__file__).with_name('Fake.csv')
        News.objects.all().delete()
        rows = []
        with csv_path.open(encoding='utf-8-sig', newline='') as file:
            for row in csv.DictReader(file):
                rows.append(News(
                    headline=row['title'].strip(),
                    body=row['text'].strip(),
                    date=datetime.strptime(row['date'].strip(), '%Y-%m-%d').date(),
                ))
        News.objects.bulk_create(rows[:5])
        self.stdout.write(self.style.SUCCESS(f'{min(len(rows), 5)} noticias cargadas correctamente.'))
