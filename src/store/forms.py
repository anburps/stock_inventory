from django import forms
from .models import *

# ----------------- FORMS -----------------
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["category_name", "description"]
    
    wedgets = {
        "category_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Category Name", "autofocus": "autofocus", "required": "required"}),
        "description": forms.Textarea(attrs={"class": "form-control", "placeholder": "Category Description", "required": "required"}),
    }

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ["name", "contact", "email", "address"]
    
    wedgets = {
        "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Supplier Name", "autofocus": "autofocus", "required": "required"}),
        "contact": forms.TextInput(attrs={"class": "form-control", "placeholder": "Supplier Contact", "required": "required"}),
        "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Supplier Email"}),
        "address": forms.Textarea(attrs={"class": "form-control", "placeholder": "Supplier Address", "required": "required"}),
    }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["user","name", "sku", "category", "supplier", 
                  "quantity", "original_price", "discount_price"]
    
    wedgets = {
        "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Product Name", "autofocus": "autofocus", "required": "required"}),
        "sku": forms.TextInput(attrs={"class": "form-control", "placeholder": "Product SKU", "required": "required"}),
        "category": forms.Select(attrs={"class": "form-control", "required": "required"}),
        "supplier": forms.Select(attrs={"class": "form-control", "required": "required"}),
        "quantity": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Product Quantity", "required": "required"}),
        "original_price": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Product Original Price", "required": "required"}),
        "discount_price": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Product Discount Price", "required": "required"}),
    }

class StockTransactionForm(forms.ModelForm):
    class Meta:
        model = StockTransaction
        fields = ["product", "transaction_type", "quantity", "note"]
    
    wedgets = {
        "product": forms.Select(attrs={"class": "form-control", "required": "required"}),
        "transaction_type": forms.Select(attrs={"class": "form-control", "required": "required"}),
        "quantity": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Transaction Quantity", "required": "required"}),
        "note": forms.Textarea(attrs={"class": "form-control", "placeholder": "Transaction Note", "required": "required"}),
    }

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = "__all__"
    
    wedgets = {
        "supplier": forms.Select(attrs={"class": "form-control", "required": "required"}),
        "note": forms.Textarea(attrs={"class": "form-control", "placeholder": "Transaction Note", "required": "required"}),
    }

class BillItemForm(forms.ModelForm):
    class Meta:
        model = BillItem
        fields = "__all__"
    
    wedgets = {
        "product": forms.Select(attrs={"class": "form-control", "required": "required"}),
        "quantity": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Transaction Quantity", "required": "required"}),
    }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = "__all__"
    
    wedgets = {
        "supplier": forms.Select(attrs={"class": "form-control", "required": "required"}),
        "note": forms.Textarea(attrs={"class": "form-control", "placeholder": "Transaction Note", "required": "required"}),
    }
    
    
    