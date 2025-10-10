from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product, StockTransaction,BillItem

@receiver(post_save, sender=Product)
def create_initial_stock_transaction(sender, instance, created, **kwargs):
    if created:
        StockTransaction.objects.create(
            product=instance,
            transaction_type=StockTransaction.IN,
            quantity=instance.quantity or 0,
            note="Initial stock added automatically when product was created."
        )


@receiver(post_save, sender=BillItem)
def create_stock_out_transaction(sender, instance, created, **kwargs):
    if created:
        StockTransaction.objects.create(
            product=instance.product,
            transaction_type=StockTransaction.OUT,
            quantity=instance.quantity,
            note=f"Stock Out for Bill #{instance.bill.id}"
        )