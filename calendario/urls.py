from django.conf.urls import url, include
from .views import (add_appointment, copy_appointments, feed, index, 
                    agendar, confirm_turn, edit_turn)


urlpatterns = [
    url(r'^$', index, name='calendario.index'),
    url(r'^feed$', feed, name='calendario.feed'),
    url(r'^feed_availables/(?P<servicio>\d+)/$', feed, name='calendario.feed-availables'),
    url(r'^appointments/$', add_appointment, name='add_appointments'),
    url(r'^appointments/copy/$', copy_appointments, name='copy_appointments'),
    url(r'^agendar/$', agendar, name='calendario.agendar'),
    url(r'^confirm_turn/(?P<pk>\d+)/$', confirm_turn, name='calendario.confirm'),
    url(r'^edit_turn/(?P<pk>\d+)/$', edit_turn, name='calendario.edit_turn'),
]
