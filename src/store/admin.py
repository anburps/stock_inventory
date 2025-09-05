from django.contrib import admin
from .models import Category, Supplier, Product, StockTransaction

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("category_name", "user", "created_at")
    search_fields = ("category_name",)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "contact")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "sku", "category", "supplier", "quantity", "original_price", "discount_price")
    list_filter = ("category", "supplier")
    search_fields = ("name", "sku")

@admin.register(StockTransaction)
class StockTransactionAdmin(admin.ModelAdmin):
    list_display = ("product", "transaction_type", "quantity", "created_at")
    list_filter = ("transaction_type",)
