from django import template

register = template.Library()

@register.simple_tag
def es_municipal_admin(user):
    #TODO: Logica para saber si tiene fucionalidades de admin de municipalidad
    return False

