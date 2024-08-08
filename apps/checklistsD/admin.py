from django.contrib import admin

from .models import ChecklistD


class ChecklistDAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "process_number", "item")


admin.site.register(ChecklistD, ChecklistDAdmin)
