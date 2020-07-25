from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render
from django.template import Context, Template

from recupero.models import Factura
from anexo2.docs import Anexo2


class Anexo2View(PermissionRequiredMixin, View):
    """ Devuelve el HTML con el Anexo II listo para imprimir
        Recibe el parametro factura_id. """

    permission_required = ("recupero.view_factura", )
    raise_exception = True

    def get(self, request, *args, **kwargs):
        factura_id = self.kwargs['factura_id']
        factura = Factura.objects.get(pk=factura_id)
        
        # Juntar los datos para el Anexo2
        data = factura.as_anexo2_json()
        anx = Anexo2(data=data)

        # Generar el Anexo2
        res = anx.get_html()

        # Si hay errores en la generación se muestran en otro template
        if res is None:

            newDict = dict()
            newDict['errors'] = anx.errors

            return render(request, template_name='recupero/anexo_errors.html', context=newDict)

        return HttpResponse(res)