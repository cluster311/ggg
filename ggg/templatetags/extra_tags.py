from django import template

register = template.Library()

@register.simple_tag
def es_municipal_admin(user):
    #TODO: Cambiar esta funcionalidad por el chequeo de que este dentro del grupo 'Municipal'
    return (user.has_perm('profesionales.can_view_tablero') | 
        user.has_perm('centros_de_salud.can_view_tablero') |
        user.has_perm('obras_sociales.can_view_tablero'))

