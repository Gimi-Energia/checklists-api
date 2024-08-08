from django.contrib import admin

from .models import ChecklistF


class ChecklistFAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "process_number", "item")


admin.site.register(ChecklistF, ChecklistFAdmin)
