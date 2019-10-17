from django.contrib import admin
from .models import Profesional
from django.conf.urls import url


class ProfesionalSite(admin.AdminSite):
    def get_urls(self):
        urls = super(CustomAdminSite, self).get_urls()
        custom_urls = [
            url(
                r"calendario$",
                self.admin_view(organization_admin.calendario),
                name="preview",
            )
        ]
        return urls + custom_urls


@admin.register(Profesional)
class ProfesionalAdmin(admin.ModelAdmin):
    list_display = ["nombres", "apellidos", "numero_documento", "matricula_profesional"]
    search_fields = [
        "nombres",
        "apellidos",
        "numero_documento",
        "matricula_profesional",
    ]
