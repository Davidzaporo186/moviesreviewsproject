from django.db import migrations


def add_url_column_if_missing(apps, schema_editor):
    Movie = apps.get_model('movie', 'Movie')
    table_name = Movie._meta.db_table
    connection = schema_editor.connection

    with connection.cursor() as cursor:
        columns = {
            column.name
            for column in connection.introspection.get_table_description(
                cursor, table_name
            )
        }

    if 'url' not in columns:
        quoted_table = schema_editor.quote_name(table_name)
        schema_editor.execute(
            f"ALTER TABLE {quoted_table} "
            "ADD COLUMN url varchar(200) NOT NULL DEFAULT ''"
        )


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            add_url_column_if_missing,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
