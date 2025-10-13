from django import forms
from .models import *

# ----------------- FORMS -----------------
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["category_name", "description"]

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ["name", "contact", "email", "address"]

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["user","name", "sku", "category", "supplier", 
                  "quantity", "original_price", "discount_price"]

class StockTransactionForm(forms.ModelForm):
    class Meta:
        model = StockTransaction
        fields = ["product", "transaction_type", "quantity", "note"]

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = "__all__"

class BillItemForm(forms.ModelForm):
    class Meta:
        model = BillItem
        fields = "__all__"

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = "__all__"
    
    
    