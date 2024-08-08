from django.contrib import admin

from .models import ChecklistE


class ChecklistEAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "process_number", "item")


admin.site.register(ChecklistE, ChecklistEAdmin)
