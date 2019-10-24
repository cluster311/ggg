from django.views.generic import TemplateView
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.conf import settings


@method_decorator(cache_page(60 * 60 * 24), name='dispatch')
class HomeView(TemplateView):
    """ Home del sistema """

    template_name = "home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["site_short_title"] = settings.SYS_SHORT_TITLE
        context["site_title"] = settings.SYS_TITLE
        context["site_description"] = settings.SYS_DESCRIPTION

        return context