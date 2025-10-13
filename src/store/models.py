from django.db import models
from django.urls import reverse
from accounts.models import User
import uuid

class Category(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    category_name   = models.CharField(max_length=100, unique=True)
    description     = models.TextField(blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    uuid            = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        ordering = ['category_name','created_at']

    def __str__(self):
        return self.category_name


class Supplier(models.Model):
    name        = models.CharField(max_length=150)
    contact     = models.CharField(max_length=100, blank=True)
    email       = models.EmailField(blank=True)
    address     = models.TextField(blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    uuid        = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        ordering = ['name','created_at']


    def __str__(self):
        return self.name


class Product(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name            = models.CharField(max_length=150)
    sku             = models.CharField(max_length=50, unique=True)
    category        = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    supplier        = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    pending_price   = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity        = models.PositiveIntegerField(default=0)
    original_price  = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_price  = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    reorder_level   = models.PositiveIntegerField(default=10) 
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    uuid            = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    
    def __str__(self):
        return f"{self.name} ({self.sku})"


    def get_absolute_url(self):
        return reverse('product_detail', args=[self.pk])


    @property
    def current_stock(self):
        ins = self.transactions.filter(transaction_type=StockTransaction.IN).aggregate(models.Sum('quantity'))['quantity__sum'] or 0
        outs = self.transactions.filter(transaction_type=StockTransaction.OUT).aggregate(models.Sum('quantity'))['quantity__sum'] or 0
        return ins - outs


class StockTransaction(models.Model):
    IN = 'IN'
    OUT = 'OUT'
    TYPE_CHOICES = [(IN, 'Stock In'), (OUT, 'Stock Out')]

    product             = models.ForeignKey(Product, related_name='transactions', on_delete=models.CASCADE)
    transaction_type    = models.CharField(max_length=3, choices=TYPE_CHOICES)
    quantity            = models.IntegerField()
    note                = models.TextField(blank=True)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)
    uuid                = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        ordering = ['-created_at']


def __str__(self):
    return f"{self.product.name} {self.transaction_type} {self.quantity}"



class Bill(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    customer        = models.CharField(max_length=150)
    purchase_total  = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid_total      = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    uuid            = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"Bill #{self.id} - {self.customer}"

    def calculate_purchase_total(self):
        total = self.items.aggregate(
            total=models.Sum(models.F('quantity') * models.F('price'), output_field=models.DecimalField())
        )['total'] or Decimal('0.00')
        self.purchase_total = total
        self.save(update_fields=['purchase_total'])
        return total

    def calculate_paid_total(self):
        total = self.payment_set.aggregate(
            total=models.Sum('amount')
        )['total'] or Decimal('0.00')
        self.paid_total = total
        self.save(update_fields=['paid_total'])
        return total

    @property
    def balance_due(self):
        """How much is still unpaid."""
        return self.purchase_total - self.paid_total


class BillItem(models.Model):
    bill        = models.ForeignKey(Bill, related_name='items', on_delete=models.CASCADE)
    product     = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity    = models.PositiveIntegerField()
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    uuid        = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    @property
    def total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.bill.calculate_purchase_total()


class Payment(models.Model):
    bill        = models.ForeignKey(Bill, on_delete=models.CASCADE)
    amount      = models.DecimalField(max_digits=10, decimal_places=2)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    uuid        = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"Payment for Bill #{self.bill.id}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.bill.calculate_paid_total()