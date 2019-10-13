from django.conf.urls import url, include
from .views import feed, index


urlpatterns = [
	url(r'^$', index, name='calendario.index'),
    url(r'^feed$', feed, name='calendario.feed'),
]