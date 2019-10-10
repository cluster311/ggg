from django.conf.urls import url, include
from .views import feed, index, add_appointment


urlpatterns = [
	url(r'^$', index, name='calendario.index'),
    url(r'^feed$', feed, name='calendario.feed'),
    url('appointment/', add_appointment, name='add_appointments')
]
