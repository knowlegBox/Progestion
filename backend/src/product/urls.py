from django.urls import path
from . import views

app_name = "product"

urlpatterns = [
  path("", views.liste_product_view, name="liste"),
  # path("", views.ListeProductView.as_view(), name="liste"),
  path('load_more/', views.load_more, name='load_more'),

  path("create/", views.create_product, name="create"),
  path('api/products/', views.product_autocomplete, name='product_autocomplete'),

  path('category/delete/<int:pk>/modal/', views.box_delete_modal, name='delete_modal'),
  path("update/<int:pk>/", views.product_update, name="update"),
  path("delete/<int:pk>/", views.delete_product, name="delete"),
  path("delete/<int:pk>/", views.DeleteCategorieView.as_view(), name="cat_delete"),
  path("categorie/delete/<int:pk>/", views.categorie_sup, name="cat_delete"),
  path("vente/journaliere/supprimer/<int:pk>/", views.DeleteVenteJour.as_view(), name="delete_vente"),

  path("vente/journaliere/create/", views.create_daylysold, name="create_vente"),

  # *-----------------------------------------* #
  # path("liste/stock/", views.NewStockList.as_view(), name="list_stock"),
  # path("create/stock/", views.NewStockCreate.as_view(), name="create_stock"),
  # path("delete/stock/<int:pk>/", views.NewStockList.as_view(), name="delete_stock"),
  # path("nouveau/produit/en stock/<int:pk>/", views.create_stock, name="tab_create_stock"),


  ]
