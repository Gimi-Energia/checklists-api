from django.contrib import admin

from .models import ChecklistA, CurrentTransformer, Transformer


class TransformerInline(admin.TabularInline):
    model = Transformer
    extra = 1


class CurrentTransformerInline(admin.TabularInline):
    model = CurrentTransformer
    extra = 1


class ChecklistAAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "process_number", "item")
    inlines = [TransformerInline, CurrentTransformerInline]


admin.site.register(ChecklistA, ChecklistAAdmin)
