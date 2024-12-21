from django.urls import path
from . import views

app_name = "facture"

urlpatterns = [
    # path("liste/commande/", views.list_commande, name="list_command"),
    # # path("liste/commande/", views.CommandlistView.as_view(), name="list_command"),
    # path("creer/commande/", views.create_command, name="create_command"),
    # path("mise-a-jour/commande/<int:pk>/", views.CommandUpdateView.as_view(), name="update_command"),
    # path("delete/commande/<int:pk>/", views.CommandDeleteView.as_view(), name="delete_command"),

    # path("enregistrement/facture", views.save_invoice, name="save"),
    # path("ajouter/nouvelle-ligne/<int:pk>/", views.add_to_invoice, name="add_line"),
    # path("nouvel/methode/<int:pk>/", views.create_new_invoice, name="invoice"),
    # path("", views.InvoiceList.as_view(), name="invoice_list"),
    path("", views.invoice_liste, name="invoice_list"),
    path('create_invoice/', views.create_invoice, name='create_invoice'),
    path("bon-commande/<int:pk>/", views.invoice_home, name="home"),
    path("produit/supprimer/<int:pk>/", views.delete_invoice_item, name="delete_line"),
    path("bon-commande/supprimer/<int:pk>/", views.delete_invoice, name="delete_invoice"),
    # path("bon-commande/supprimer/<int:pk>/", views.InvoiceDeleteView.as_view(), name="delete_invoice"),

    path('detail/<int:invoice_id>/', views.invoice_detail, name='invoice_detail'),

    path('add_to_invoice/<int:pk>/', views.add_to_invoice, name='add_line'),
    path('modifier/ligne/de bon/commnde/<int:pk>/', views.invoice_item_edite, name='invoice_item_edit'),

]
