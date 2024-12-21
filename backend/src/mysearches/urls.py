from django.urls import path

from mysearches import views

app_name = "search"
urlpatterns = [
    path("", views.product_search, name="product"),
    path("invoices/supplier/", views.invoice_search_supplier, name="invoice_supplier"),
    path("invoices/client/", views.invoice_search_client, name="invoice_client"),
    path("table/seach/", views.product_list_seach, name="table_search"),

    # path('upload-products/', views.upload_products, name='upload_products'),

]
