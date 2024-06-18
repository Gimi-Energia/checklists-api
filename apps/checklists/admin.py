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
        "budget_number",
        "client_name",
        "client_email",
        "answered_registration",
        "answered_optional",
        "created_at",
    )
    inlines = [ChecklistProductInline]


class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


admin.site.register(Checklist, ChecklistAdmin)
admin.site.register(Product, ProductAdmin)
