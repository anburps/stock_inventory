from django.urls import path
from . import views
from accounts import views as account
urlpatterns = [
    path("register/", account.register_view, name="register"),
    path("", account.login_view, name="login"),
    path("logout/", account.logout_view, name="logout"),
    
    path("index/", views.index, name="index"),
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
    
    # Bill
    path("bills-list/", views.bill_list, name="bill_list"),
    path("bills-create/", views.create_bill, name="bill_create"),
    path("bill-detail/<int:pk>/", views.bill_detail, name="bill_detail"),
    path("bills/<int:pk>/update/", views.bill_update, name="bill_update"),
    path('get-product-price/<int:product_id>/', views.get_product_price, name='get_product_price'),

    
    # BillItem
    # path("billitems/create/", views.billitem_create, name="billitem_create"),
    path("billitems/list/", views.billitem_list, name="billitem_list"),
    path("billitems/<int:pk>/detail/", views.billitem_detail, name="billitem_detail"),
    path("billitems/<int:pk>/update/", views.billitem_update, name="billitem_update"),
    
    # Payments
    path("payments_create/<int:id>/", views.create_payment, name="payment_create"),
    path("payments_list/", views.payment_list, name="payment_list"),
    path("payments/<int:pk>/detail/", views.payment_detail, name="payment_detail"),
    path("payments/<int:pk>/update/", views.payment_update, name="payment_update"),
]
