from django.conf.urls import url, include
from django.urls import path
from .views import (FacturaListView,
                    FacturaDetailView,
                    FacturaUpdateView,
                    FacturaCreateView)

from .views_tipo_prestacion import (TipoPrestacionListView,
                                    TipoPrestacionCreateView,
                                    TipoPrestacionDetailView,
                                    TipoPrestacionUpdateView)

from .views_tipo_documento_anexo import (TipoDocumentoAnexoListView,
                                         TipoDocumentoAnexoCreateView,
                                         TipoDocumentoAnexoDetailView,
                                         TipoDocumentoAnexoUpdateView)

urlpatterns = [
    url(
        r"^facturacion$",
        FacturaListView.as_view(),
        name="recupero.facturas",
    ),
    path(
        r"detalle-factura/<int:pk>",
        FacturaDetailView.as_view(),
        name="recupero.factura.detail",
    ),
    path(
        r"editar-factura/<int:pk>",
        FacturaUpdateView.as_view(),
        name="recupero.factura.edit",
    ),
    path(
        r"crear-factura",
        FacturaCreateView.as_view(),
        name="recupero.factura.create",
    ),
    path(
        r"tipo-de-prestacion.html",
        TipoPrestacionListView.as_view(),
        name="recupero.tipos-prestacion",
    ),
    path(
        r"crear-tipo-de-prestacion.html",
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

    url(
        r"^tipo-de-documentacion-anexa.html$",
        TipoDocumentoAnexoListView.as_view(),
        name="recupero.tipos-doc-anexo",
    ),
    path(
        r"crear-tipo-de-documentacion.html",
        TipoDocumentoAnexoCreateView.as_view(),
        name="recupero.tipos-documento-anexo.create",
    ),
    path(
        r"detalle-tipo-de-documentacion/<int:pk>",
        TipoDocumentoAnexoDetailView.as_view(),
        name="recupero.tipos-documento-anexo.detail",
    ),
    path(
        r"editar-tipo-de-documentacion/<int:pk>",
        TipoDocumentoAnexoUpdateView.as_view(),
        name="recupero.tipos-documento-anexo.edit",
    ),
    
]

