from django.contrib import admin

from .models import ChecklistG


class ChecklistGAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "process_number")


admin.site.register(ChecklistG, ChecklistGAdmin)
