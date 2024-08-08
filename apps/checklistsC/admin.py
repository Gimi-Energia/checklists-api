from django.contrib import admin

from .models import ChecklistC


class ChecklistCAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "process_number", "item")


admin.site.register(ChecklistC, ChecklistCAdmin)
