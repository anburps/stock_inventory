from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product, StockTransaction,BillItem
from django.db import models

@receiver(post_save, sender=Product)
def create_initial_stock_transaction(sender, instance, created, **kwargs):
    if created:
        StockTransaction.objects.create(
            product=instance,
            transaction_type=StockTransaction.IN,
            quantity=instance.quantity or 0,
            quantity_stock_out=0,
            quantity_stock_in=instance.quantity or 0,
            note="Initial stock added automatically when product was created."
        )

@receiver(post_save, sender=BillItem)
def create_stock_out_transaction(sender, instance, created, **kwargs):
    
    if created:
        product = instance.product

        if product.quantity >= instance.quantity:
            product.quantity -= instance.quantity
        else:
            product.quantity = 0
        product.save(update_fields=["quantity"])

        last_txn = product.transactions.order_by('-created_at').first()

        if last_txn:
            prev_in = last_txn.quantity_stock_in
            prev_out = last_txn.quantity_stock_out
        else:
            prev_in = product.quantity 
            prev_out = 0

        StockTransaction.objects.create(
            product=product,
            transaction_type=StockTransaction.OUT,
            quantity=instance.quantity,
            quantity_stock_in=prev_in-instance.quantity,  
            quantity_stock_out=prev_out + instance.quantity,  
            note=f"Stock Out for Bill #{instance.bill.id}"
        )

        print(f"Product: {product.name} | IN: {prev_in} | OUT: {prev_out + instance.quantity} | Current Stock: {product.quantity}")
