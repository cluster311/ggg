from django.http import HttpResponse
from django.views import View
from django.template import Context, Template

from recupero.models import Factura
from anexo2.docs import Anexo2


class Anexo2View(View):
    """ Devuelve el HTML con el Anexo II listo para imprimir
        Recibe el parametro factura_id. """
    
    permission_required = ("recupero.view_factura", )

    def get(self, request, *args, **kwargs):
        factura_id = self.kwargs['factura_id']
        factura = Factura.objects.get(pk=factura_id)
        
        data = factura.as_anexo2_json()
        anx = Anexo2(data=data)
        res = anx.get_html()
        if res is None:
            res = '<h1>ERRORES al procesar pedido</h1>'
            res += '<ul>'
            for field, error in anx.errors.items():
                res += f'<li>{field}: {error}</li>'
            res += '</ul>'

        return HttpResponse(res)