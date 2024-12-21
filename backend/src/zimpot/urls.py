from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import settings
from .views import index, product_by_categorie, dashbord, category_autocomplete

urlpatterns = [
    path('admin/', admin.site.urls),
    path("home/", index, name="myhome"),
    path("", dashbord, name="dashboard"),

    path("categorie/produit/<int:pk>/", product_by_categorie, name="cat_prod"),
    path('category-autocomplete/', category_autocomplete, name='category_autocomplete'),
    path("customer/", include("customers.urls", namespace="customer")),
    path("product/", include("product.urls", namespace="product")),
    path("facture/", include("facture.urls", namespace="facture")),
    path("fournisseur/", include("supplier.urls", namespace="supplier")),
    path("transactions/", include("transactions.urls", namespace="transactions")),
    path("compte/", include("account.urls", namespace="account")),
    path("recherche/", include("mysearches.urls", namespace="search")),
    path("pdf/", include("paperhandle.urls", namespace="pdf")),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


