from django.contrib import admin

from .models import ChecklistB


class ChecklistBAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "process_number", "item")


admin.site.register(ChecklistB, ChecklistBAdmin)
