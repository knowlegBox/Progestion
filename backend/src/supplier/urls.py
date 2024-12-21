from django.urls import path
from . import views

app_name = "supplier"
urlpatterns = [
    path('', views.supplier_list, name='supplier_list'),
    path('detail/<int:supplier_id>/', views.supplier_detail, name='supplier_detail'),
    path('creer-nouveau/new/', views.supplier_create, name='supplier_create'),
    path('mettre-a-jour/<int:supplier_id>/edit/', views.supplier_update, name='supplier_update'),
    path('supprimer/<int:supplier_id>/delete/', views.supplier_delete, name='supplier_delete'),

    # path("", views.SupplierInvoiceList.as_view(), name="invoice_list"),
    # path('create_invoice/', views.create_invoice, name='create_invoice'),
    path("bon-commande/<int:pk>/", views.invoice_home, name="home"),
    # path("produit/supprimer/<int:pk>/", views.delete_invoice_item, name="delete_line"),
    path("bon-commande/supprimer/<int:pk>/", views.delete_invoice, name="delete_invoice"),

    path('detail/bon-commande/<int:invoice_id>/', views.invoice_detail, name='invoice_detail'),
    path('create_invoice/', views.create_invoice, name='create_invoice'),

    path('add_to_invoice/<int:pk>/', views.add_to_invoice, name='add_line'),
    path("depot-depot/<int:pk>/", views.create_depot, name="create_dep"),

    path("liste/stock/", views.SupplierInvoiceItemsList.as_view(), name="list_stock"),
    path("create/stock/", views.SupplierInvoiceItemsCreate.as_view(), name="create_stock"),
    path("delete/stock/<int:pk>/", views.delete_invoice_item, name="delete_line"),
    # path("delete/stock/<int:pk>/", views.SupplierInvoiceItemsDelete.as_view(), name="delete_line"),
    path("nouveau/produit/en stock/<int:pk>/", views.create_stock, name="tab_create_stock"),

    #     path('modifier/ligne/de bon/commnde/<int:pk>/', views.invoice_item_edite, name='invoice_item_edit'),

]
