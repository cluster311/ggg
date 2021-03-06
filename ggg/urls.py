from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import url, include
from django.contrib.staticfiles.urls import static
from .views import (LandingPage, choice_homepage, 
                   CiudadanoHome, RecuperoHome, SuperAdminHome, DataHome )



urlpatterns = [
    # url(r'^jet/', include('jet.urls', 'jet')),
    path('admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^core/', include('core.urls')),
    url(r'^profesionales/', include('profesionales.urls')),
    url(r'^turnos/', include('calendario.urls')),
    url(r'^obras-sociales/', include('obras_sociales.urls')),
    url(r'^centros_de_salud/', include('centros_de_salud.urls')),
    url(r'^recupero/', include('recupero.urls')),
    url(r'^especialidades/', include('especialidades.urls')),
    url(r'^usuarios/', include('usuarios.urls')),
    url(r'^pacientes/', include('pacientes.urls')),
    url(r'^$', LandingPage.as_view(), name='landing'),
    url(r'^ciudadano/$', CiudadanoHome.as_view(), name='ciudadano.home'),
    url(r'^hsuper/$', SuperAdminHome.as_view(), name='super.home'),
    url(r'^hrecupero/$', RecuperoHome.as_view(), name='recupero.home'),
    url(r'^hdata/$', DataHome.as_view(), name='data.home'),
    url(r'^home/$', choice_homepage, name='home'),
] 

handler403 = 'core.views.handler403'

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
