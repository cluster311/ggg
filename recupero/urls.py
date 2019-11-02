from django.conf.urls import url, include
from django.urls import path
from .views import (
    FacturaPendEnvioView,
    FacturaPendCobroView,
    TipoDocAnexoView
)
from .views_tipo_prestacion import (TipoPrestacioListView,
                                    TipoPrestacionCreateView,
                                    TipoPrestacionDetailView,
                                    TipoPrestacionUpdateView)


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
        TipoPrestacioListView.as_view(),
        name="recupero.tipos-prestacion",
    ),
    path(
        r"crear-tipo-de-prestacio.html",
        TipoPrestacionCreateView.as_view(),
        name="recupero.tipos-prestacion.create",
    ),
    path(
        r"detalle-tipo-de-prestacion/<int:pk>",
        TipoPrestacionDetailView.as_view(),
        name="recupero.tipos-prestacion.detail",
    ),
    path(
        r"editar-tipo-de-prestacion/<int:pk>",
        TipoPrestacionUpdateView.as_view(),
        name="recupero.tipos-prestacion.edit",
    ),
]

