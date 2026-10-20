from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('movie', '0001_initial'),
    ]

    # The production SQLite database never had movie_movie.url.
    # This is a state-only migration so existing AWS databases are not altered.
    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.RemoveField(
                    model_name='movie',
                    name='url',
                ),
            ],
        ),
    ]
