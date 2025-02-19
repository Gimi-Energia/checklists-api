from django.contrib import admin

from .models import Checklist, ChecklistProduct, Product


class ChecklistProductInline(admin.TabularInline):
    model = ChecklistProduct
    extra = 1


class ChecklistAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "company",
        "process_number",
        "auxiliary_number",
        "construction_name",
        "client_name",
        "client_email",
    )
    inlines = [ChecklistProductInline]


class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


admin.site.register(Checklist, ChecklistAdmin)
admin.site.register(Product, ProductAdmin)
