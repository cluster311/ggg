from django.http import HttpResponse
from django.views import View
from django.template import Context, Template

from pacientes.models import Consulta
from anexo2.docs import Anexo2


class Anexo2View(View):
    """ Devuelve el HTML con el Anexo II listo para imprimir
        Recibe el parametro consulta_id. """
    
    permission_required = ("recupero.view_factura", )

    def get_context_data(self, **kwargs):
        consulta_id = self.kwargs['consulta_id']
        consulta = Consulta.objects.get(pk=consulta_id)
        context = super().get_context_data(**kwargs)

        return context


    def get(self, request, *args, **kwargs):
        
        
        anx = Anexo2(data=data)
        save_to = 'path.html'
        res = anx.get_html(save_path=save_to)
        if res is None:
            print('ERRORES al procesar pedido')
            for field, error in a2.errors.items():
                print(f' - {field}: {error}')
        else:
            print(f'Procesado correctamente y grabado en {save_to}')

        template = Template("My name is {{ my_name }}.")
        context = Context({"my_name": "Adrian"})
        template.render(context)

        return HttpResponse('Hello, World!')