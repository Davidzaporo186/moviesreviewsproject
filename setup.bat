@echo off
echo Instalando dependencias...
python -m pip install -r requirements.txt
if errorlevel 1 pause & exit /b 1
echo Ejecutando migraciones...
python manage.py migrate
if errorlevel 1 pause & exit /b 1
echo Cargando peliculas...
python manage.py add_movies_db
echo Cargando noticias...
python manage.py add_news_db
echo.
echo Listo. Ejecuta: python manage.py runserver
pause
