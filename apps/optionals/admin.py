from django.contrib import admin

from .models import Optional


class OptionalAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "process_number")


admin.site.register(Optional, OptionalAdmin)
