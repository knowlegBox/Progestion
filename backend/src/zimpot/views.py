from customers.models import Customer
from product.models import Product, Category, VenteJournaliere
from supplier.models import Supplier, SupplierInvoices
from transactions.models import DailySpend
from django.db.models import Sum, Q

from django.shortcuts import render
from django.utils import timezone


def index(request):
    try:
        categorie = Category.objects.only("name").all()
        vente_jour = VenteJournaliere.objects.all()[:10]
        context = {
            # "product": product,
            "category": categorie,
            "produit_dispo": vente_jour
        }
        return render(request, "base.html", context)
    except Exception as e:
        return render(request, "base.html")


def product_by_categorie(requests, pk):
    categorie = Category.objects.only("name").get(pk=pk)
    produit = categorie.products.all()
    produit_sum = categorie.products.all().aggregate(somme_total=Sum("quantity"))["somme_total"]

    return render(requests, "global/table.html", context={
        "product": produit,
        "qtite": produit_sum,
        "cat": categorie})


def category_autocomplete(request):
    query = request.GET.get("query", "")
    categories = Category.objects.filter(name__icontains=query)[:5]
    return render(request, 'cate_auto_complete.html', {"categories": categories})


def dashbord(request):
    month_date = timezone.now().month
    all_client = Customer.objects.all()
    client_number = all_client.count()
    supplier = Supplier.objects.all().count()
    spend = DailySpend.objects.only("value", "add_date").filter(add_date__month=month_date).aggregate(total = Sum("value"))['total'] or 0
    # supp_debt = SupplierInvoices.objects.only("total_price", "date").filter(date__month= month_date).aggregate(total=Sum("total_price"))["total"] or 0
    supp_debt = Supplier.objects.filter(solde__gt=0).aggregate(total=Sum("solde"))["total"] or 0
    client_debt = all_client.filter(solde__gt=0).aggregate(total= Sum("solde"))["total"] or 0
    monthly_solde = VenteJournaliere.objects.all().filter(add_date__month=month_date).aggregate(total=Sum("totalprice"))["total"] or 0
    context = {
        "customer": client_number,
        "client_debt": client_debt,
        "supplier": supplier,
        "spend": spend,
        "supp_debt": supp_debt,
        'monthly_solde': monthly_solde
    }
    return render(request, "dashboard/dashboad.html", context)
# def ventes_mois_en_cours(request):
#     # Obtenir la date actuelle
#     today = timezone.now()
#
#     # Filtrer les ventes pour le mois en cours
#     ventes_mois = VenteJournaliere.objects.filter(
#         add_date__year=today.year,
#         add_date__month=today.month
#     ).values('product__name').annotate(total_vendu=Sum('totalprice'))
#
#     # Passer les données au template
#     context = {
#         'ventes_mois': ventes_mois,
#     }
#
#     return render(request, 'dashboard/ventes_mois.html', context)
#
#
# class ProduitsMoisView(ListView):
#     template_name = 'produits_mois.html'
#     context_object_name = 'produits_vendus'
#
#     def get_queryset(self):
#         # Calculer le premier jour du mois en cours
#         today = timezone.now()
#         start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
#
#         # Récupérer et agréger les ventes du mois
#         produits_vendus = VenteJournaliere.objects.filter(
#             vente__date__gte=start_of_month,
#             vente__date__lte=today
#         ).annotate(
#             total_vendu=Sum('vente__quantite')
#         ).values('nom', 'total_vendu').order_by('-total_vendu')
#
#         return produits_vendus
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['mois_actuel'] = timezone.now().strftime('%B %Y')
#         return context


# def dashbord(requests):
#     data = dette_client()  # return client account
#     custom_det = data[0]  # all client debt value sum
#     client_dete = data[1]  # one client and the value of him debt
#     all_customer = data[2]
#     vente_mensuelle()
#     # all_product = Product.objects.all()
#     all_categories = Category.objects.all()
#     # resoudre le probleme avec la catégorie ensuite le produit et enfin la vente journaliere
#     for categorie in all_categories:
#         all_product = categorie.products.all()
#         # print([categorie,all_product])
#         for products in all_product:
#             month_solde = VenteJournaliere.objects.filter(product=products.pk)
#             # print(month_solde)
#
#     # resoudre le probleme avec le produit et enfin la vente journaliere
#     # all_product = Product.objects.only("pk").all()
#     # for prod in all_product:
#     # produit = prod.produit_vendu.all()
#     # print(produit)
#     # month_solde = VenteJournaliere.objects.filter(product=pk)
#     # print(month_solde)
#     today = timezone.now()
#
#     # Filtrer les ventes pour le mois en cours
#     ventes_mois = VenteJournaliere.objects.filter(
#         add_date__year=today.year,
#         add_date__month=today.month
#     ).values('product__name').annotate(total_vendu=Sum('totalprice'))
#
#     # depense = DailySpend.objects.filter(
#     #     add_date__year=today.year,
#     #     add_date__month=today.month
#     # ).aggregate(total=Sum("value"))["total"] or 0
#     depense = DailySpend.objects.only("value").all()
#     context = {
#         "custom_det": custom_det,
#         "client_dete": client_dete,
#         "all_customer": all_customer,
#         'ventes_mois': ventes_mois,
#         "depense": depense
#     }
#     return render(requests, "dashboard/dashboad.html", context)
