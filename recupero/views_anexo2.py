from django.http import HttpResponse
from django.views import View


class Anexo2View(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, World!')