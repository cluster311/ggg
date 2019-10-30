from django.conf.urls import url, include
from django.urls import path
from .views import (
    FacturaPendEnvioView,
    FacturaPendCobroView,
    TipoDocAnexoView,
    TipoPrestacioView
)


urlpatterns = [
    url(
        r"^facturacion-pendiente-de-envio.html$",
        FacturaPendEnvioView.as_view(),
        name="recupero.factura.lista-pendientes-envio",
    ),
    url(
        r"^facturacion-pendiente-de-cobro.html$",
        FacturaPendCobroView.as_view(),
        name="recupero.factura.lista-pendientes-cobro",
    ),
    url(
        r"^tipo-de-documentacion-anexa.html$",
        TipoDocAnexoView.as_view(),
        name="recupero.tipos-doc-anexo",
    ),
    path(
        r"tipo-de-prestacio.html",
        TipoPrestacioView.as_view(),
        name="recupero.tipos-prestacion",
    ),
]
