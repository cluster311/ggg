from django.conf.urls import url, include
from .views import add_appointment, copy_appointments, feed, index


urlpatterns = [
    url(r'^$', index, name='calendario.index'),
    url(r'^feed$', feed, name='calendario.feed'),
    url(r'^appointments/$', add_appointment, name='add_appointments'),
    url(r'^appointments/copy/$', copy_appointments, name='copy_appointments'),
]
