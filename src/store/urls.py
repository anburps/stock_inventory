from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    # Category
    path("categories/", views.category_list, name="category_list"),
    path("categories/create/", views.category_create, name="category_create"),
    path("categories/<int:pk>/update/", views.category_update, name="category_update"),
    path("categories/<int:pk>/delete/", views.category_delete, name="category_delete"),

    # Supplier
    path("suppliers/", views.supplier_list, name="supplier_list"),
    path("suppliers/create/", views.supplier_create, name="supplier_create"),
    path("suppliers/<int:pk>/update/", views.supplier_update, name="supplier_update"),
    path("suppliers/<int:pk>/delete/", views.supplier_delete, name="supplier_delete"),

    # Product
    path("products/", views.product_list, name="product_list"),
    path("products/create/", views.product_create, name="product_create"),
    path("products/<int:pk>/", views.product_detail, name="product_detail"),
    path("products/<int:pk>/update/", views.product_update, name="product_update"),
    path("products/<int:pk>/delete/", views.product_delete, name="product_delete"),

    # Stock Transaction
    path("transactions/", views.transaction_list, name="transaction_list"),
    path("transactions/create/", views.transaction_create, name="transaction_create"),
]
