# Movies Reviews - Taller 2

Proyecto Django preparado según el Taller 2 de Frontend y BD.

## Instalación rápida

En PowerShell, dentro de esta carpeta:

```powershell
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py add_movies_db
python manage.py add_news_db
python manage.py runserver
```

Luego abre:
- http://127.0.0.1:8000/
- http://127.0.0.1:8000/news/
- http://127.0.0.1:8000/statistics/
- http://127.0.0.1:8000/about/

## Búsqueda

La búsqueda funciona con `?searchMovie=` y también acepta `?search=`.

## GitHub

El proyecto incluye commits de ejemplo con los mensajes solicitados por el taller. Para conectarlo al repositorio del estudiante:

```powershell
git remote add origin https://github.com/Davidzaporo186/moviesreviewsproject.git
git push -u origin main
```

Si GitHub rechaza el push porque ya tiene otro historial, primero respalda el repositorio remoto y luego decide si usar `git push --force-with-lease` o integrar ambos historiales.
