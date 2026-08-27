from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from movie import views as movie_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('movie.urls')),
    path('news/', include('news.urls')),
    path('signup/', movie_views.signup, name='signup'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
