from django.urls import path
from . import views

app_name = "transaction"


urlpatterns = [
    path("", views.list_transaction, name="liste"),

    # path("create-retrait", views.CreateWithdrallView.as_view(), name="create_wid"),
    # path("create-retrait/", views.create_retrait, name="create_wid"),
    # path("retrait-update/<int:pk>/", views.UpdateWithdrallView.as_view(), name="update_wid"),
    # path("retrait-delete/<int:pk>/", views.DeleteWithdrallView.as_view(), name="delete_wid"),
    path("facture-delete/<int:pk>/", views.facture_delete, name="delete_wid"),

    # ----------------------------- Depots ------------------------------
    # path("depot-depot/", views.CreateDepotView.as_view(), name="create_dep"),
    path("depot-depot/<int:pk>/", views.create_depot, name="create_dep"),
    # path("depot-update/<int:pk>/", views.UpdateVersementView.as_view(), name="update_dep"),
    # path("depot-delete/<int:pk>/", views.DeleteDepotView.as_view(), name="delete_dep"),
    path("versement-delete/<int:pk>/", views.versement_delete, name="delete_dep"),


    path("enregistrer/depenses-journalieres/", views.SpendCreateView.as_view(), name="create_spend"),
    # path("enregistrer/depenses-journalieres/", views.create_daylyspend, name="create_spend"),
    path("liste/depenses-journalieres/", views.SpendListeView.as_view(), name="liste_spend"),
    path("supprimer/depenses-journalieres/<int:pk>/", views.SpendDeleteView.as_view(), name="delete_spend"),



]
