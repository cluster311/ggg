from django.conf.urls import url, include
from .views import add_appointment, copy_appointments, feed, index, agendar


urlpatterns = [
    url(r'^$', index, name='calendario.index'),
    url(r'^feed$', feed, name='calendario.feed'),
    url(r'^feed/(?P<servicio>\d+)/$', feed, name='calendario.feed'),
    url(r'^appointments/$', add_appointment, name='add_appointments'),
    url(r'^appointments/copy/$', copy_appointments, name='copy_appointments'),
    url(r'^agendar/$', agendar, name='calendario.agendar'),
]
