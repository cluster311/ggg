from django.views.generic import TemplateView
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.conf import settings


class HomeView(TemplateView):
    """ Home del sistema """
    template_name = "home.html"