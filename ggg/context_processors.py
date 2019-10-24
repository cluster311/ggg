from django.conf import settings


def cpp_settings(request):
    context = {}
    context["site_short_title"] = settings.SYS_SHORT_TITLE
    context["site_title"] = settings.SYS_TITLE
    context["site_description"] = settings.SYS_DESCRIPTION
    return context