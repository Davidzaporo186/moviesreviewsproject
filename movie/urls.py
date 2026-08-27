from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_movies, name='search_movies'),
    path('about/', views.about, name='about'),
    path('statistics/', views.statistics_view, name='statistics'),
]
