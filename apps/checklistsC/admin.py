from django.contrib import admin

from .models import ChecklistC, Consumer, CurrentTransformer, Transformer


class TransformerInline(admin.TabularInline):
    model = Transformer
    extra = 1


class CurrentTransformerInline(admin.TabularInline):
    model = CurrentTransformer
    extra = 1


class ConsumerInline(admin.TabularInline):
    model = Consumer
    extra = 1
    inlines = [TransformerInline]


class ChecklistCAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "process_number", "item")
    inlines = [ConsumerInline, CurrentTransformerInline]


admin.site.register(ChecklistC, ChecklistCAdmin)
