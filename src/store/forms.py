from django import forms
from .models import Category, Supplier, Product, StockTransaction

# ----------------- FORMS -----------------
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["user", "category_name", "description"]

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ["name", "contact", "email", "address"]

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "sku", "category", "supplier", "pending_price", 
                  "quantity", "original_price", "discount_price", "reorder_level"]

class StockTransactionForm(forms.ModelForm):
    class Meta:
        model = StockTransaction
        fields = ["product", "transaction_type", "quantity", "note"]
