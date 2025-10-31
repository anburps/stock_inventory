from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import  *
from django.db.models import Sum
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.


# ----------------- INDEX -----------------
def index(request):
    stock_in = StockTransaction.objects.filter(transaction_type="IN").aggregate(Sum("quantity"))["quantity__sum"] or 0
    stock_out = StockTransaction.objects.filter(transaction_type="OUT").aggregate(Sum("quantity"))["quantity__sum"] or 0

    context = {
        "category_count": Category.objects.count(),
        "supplier_count": Supplier.objects.count(),
        "product_count": Product.objects.count(),
        "transaction_count": StockTransaction.objects.count(),
        "recent_transactions": StockTransaction.objects.select_related("product").order_by("-created_at")[:5],
        "stock_in": stock_in,
        "stock_out": stock_out,
        "categories": Category.objects.all(),
    }
    return render(request, "inventory/index.html",context)

# ----------------- CATEGORY -----------------


def category_list(request):
    search_query = request.GET.get("search", "")
    categories = Category.objects.all()

    if search_query:
        categories = categories.filter(category_name__icontains=search_query)

    # Pagination
    paginator = Paginator(categories, 4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # AJAX check
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string("inventory/category_table.html", {"categories": page_obj})
        return JsonResponse({"html": html})

    return render(request, "inventory/category_list.html", {"categories": page_obj, "search_query": search_query})

@login_required
def category_create(request):
    user = request.user
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = user
            form.save()
            return redirect("category_list")
    else:
        form = CategoryForm()
    return render(request, "inventory/category_create.html", {"form": form})

def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect("category_list")
    else:
        form = CategoryForm(instance=category)
    return render(request, "inventory/category_edit.html", {"form": form})

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.delete()
        return redirect("category_list")
    return render(request, "inventory/confirm_delete.html", {"object": category})

# ----------------- SUPPLIER -----------------
def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, "inventory/supplier_list.html", {"suppliers": suppliers})

@login_required
def supplier_create(request):
    user = request.user
    if request.method == "POST":
        form = SupplierForm(request.POST)
        if form.is_valid():
            data=form.save(commit=False)
            data.user = user
            data.save()
            
            return redirect("supplier_list")
    else:
        form = SupplierForm()
    return render(request, "inventory/supplier_create.html", {"form": form})

def supplier_update(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == "POST":
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect("supplier_list")
    else:
        form = SupplierForm(instance=supplier)
    return render(request, "inventory/form.html", {"form": form})

def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == "POST":
        supplier.delete()
        return redirect("supplier_list")
    return render(request, "inventory/confirm_delete.html", {"object": supplier})

# ----------------- PRODUCT -----------------
def product_list(request):
    products = Product.objects.all()
    return render(request, "inventory/product_list.html", {"products": products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "inventory/product_detail.html", {"product": product})

@login_required
def product_create(request):
    user = request.user
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            data=form.save(commit=False)
            data.user = user
            data.save()
            return redirect("product_list")
    else:
        form = ProductForm()
    return render(request, "inventory/product_create.html", {"form": form})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect("product_list")
    else:
        form = ProductForm(instance=product)
    return render(request, "inventory/form.html", {"form": form})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect("product_list")
    return render(request, "inventory/confirm_delete.html", {"object": product})

# ----------------- STOCK TRANSACTION -----------------
def transaction_list(request):
    transactions = StockTransaction.objects.select_related("product").all()
    return render(request, "inventory/transaction_list.html", {"transactions": transactions})

@login_required
def transaction_create(request):
    user = request.user
    if request.method == "POST":
        form = StockTransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = user
            # Auto-update product stock
            if transaction.transaction_type == StockTransaction.IN:
                transaction.product.quantity += transaction.quantity
            elif transaction.transaction_type == StockTransaction.OUT:
                transaction.product.quantity -= transaction.quantity
            transaction.product.save()
            return redirect("transaction_list")
    else:
        form = StockTransactionForm()
    return render(request, "inventory/form.html", {"form": form})

# ✅ Create Bill with multiple BillItems
def create_bill(request):
    if request.method == 'POST':
        bill_form = BillForm(request.POST)
        formset = BillItemFormSet(request.POST)

        if bill_form.is_valid() and formset.is_valid():
            bill = bill_form.save(commit=False)
            bill.user = request.user
            bill.save()

            items = formset.save(commit=False)
            for item in items:
                item.bill = bill
                item.save()
            formset.save_m2m()

            bill.calculate_purchase_total()
            messages.success(request, "Bill created successfully.")
            return redirect('bill_detail', bill.id)
    else:
        bill_form = BillForm()
        formset = BillItemFormSet()

    context = {
        'bill_form': bill_form,
        'formset': formset,
    }
    return render(request, 'inventory/bill_create.html', context)


# ✅ View to create Payment for a Bill
def create_payment(request, id):
    bill = get_object_or_404(Bill, id=id)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.bill = bill
            payment.save()
            bill.calculate_paid_total()
            messages.success(request, f"Payment added for Bill #{bill.id}")
            return redirect('bill_detail', bill.id)
    else:
        form = PaymentForm(initial={'bill': bill})

    context = {
        'form': form,
        'bill': bill,
    }
    return render(request, 'inventory/payment_create.html', context)

def bill_list(request):
    bills = Bill.objects.all()
    return render(request, "inventory/bill_list.html", {"bills": bills})


def bill_detail(request, pk):
    bill = get_object_or_404(Bill, id=pk)
    items = bill.items.all()
    payments = bill.payments.all()

    context = {
        'bill': bill,
        'items': items,
        'payments': payments,
    }
    return render(request, "inventory/bill_details.html", context)

def bill_update(request, pk):
    bill = get_object_or_404(Bill, pk=pk)
    if request.method == "POST":
        form = BillForm(request.POST, instance=bill)
        if form.is_valid():
            form.save()
            return redirect("bill_list")
    else:
        form = BillForm(instance=bill)
    return render(request, "inventory/form.html", {"form": form})


def billitem_list(request):
    billitems = BillItem.objects.all()
    return render(request, "inventory/billitem_list.html", {"billitems": billitems})
    
def billitem_detail(request, pk):
    bill = get_object_or_404(BillItem, pk=pk)
    return render(request, "inventory/billitem_detail.html", {"bill": bill})

def billitem_update(request, pk):
    billitem = get_object_or_404(BillItem, pk=pk)
    if request.method == "POST":
        form = BillItemForm(request.POST, instance=billitem)
        if form.is_valid():
            form.save()
            return redirect("bill_list")
    else:
        form = BillItemForm(instance=billitem)
    return render(request, "inventory/form.html", {"form": form})

def payment_list(request):
    payments = Payment.objects.all()
    return render(request, "inventory/payment_list.html", {"payments": payments})

def payment_detail(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    return render(request, "inventory/payment_detail.html", {"payment": payment})
    
def payment_update(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.method == "POST":
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            return redirect("bill_list")
    else:
        form = PaymentForm(instance=payment)
    return render(request, "inventory/form.html", {"form": form})