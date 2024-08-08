from django.contrib import admin

from .models import ChecklistD, Transformer


class TransformerInline(admin.TabularInline):
    model = Transformer
    extra = 1


class ChecklistDAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "process_number", "item")
    inlines = [TransformerInline]


admin.site.register(ChecklistD, ChecklistDAdmin)
