from django.views.generic import TemplateView
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.conf import settings


@method_decorator(cache_page(60 * 60 * 24), name='dispatch')
class HomeView(TemplateView):
    """ Home del sistema """
    template_name = "home.html"