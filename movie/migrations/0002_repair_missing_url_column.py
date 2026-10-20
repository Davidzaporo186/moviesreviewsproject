from django.db import migrations


def repair_movie_url(apps, schema_editor):
    connection = schema_editor.connection
    table = 'movie_movie'
    with connection.cursor() as cursor:
        existing_tables = connection.introspection.table_names(cursor)
        if table not in existing_tables:
            return
        columns = {col.name for col in connection.introspection.get_table_description(cursor, table)}
    if 'url' not in columns:
        schema_editor.execute(
            'ALTER TABLE "movie_movie" ADD COLUMN "url" varchar(200) NOT NULL DEFAULT \'\''
        )


class Migration(migrations.Migration):
    dependencies = [('movie', '0001_initial')]
    operations = [migrations.RunPython(repair_movie_url, migrations.RunPython.noop)]
