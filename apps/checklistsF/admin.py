from django.contrib import admin

from .models import ChecklistF, CurrentTransformer, Transformer


class TransformerInline(admin.TabularInline):
    model = Transformer
    extra = 1


class CurrentTransformerInline(admin.TabularInline):
    model = CurrentTransformer
    extra = 1


class ChecklistFAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "process_number", "item")
    inlines = [TransformerInline, CurrentTransformerInline]


admin.site.register(ChecklistF, ChecklistFAdmin)
