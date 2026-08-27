from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('image', models.ImageField(default='movie/images/default.jpg', upload_to='movie/images')),
                ('url', models.URLField(blank=True)),
                ('genre', models.CharField(max_length=200)),
                ('year', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
