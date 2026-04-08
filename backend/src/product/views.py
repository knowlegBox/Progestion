import datetime
import json

from django.core.paginator import Paginator
from django.forms import formset_factory
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views import generic

from customers.models import Customer
from product.form import ProductForm, VentJournaliereform
from django.db.models import Sum, F
from django.utils import timezone
from .models import Product, Category, VenteJournaliere
from zimpot.utilitaire import new_hold_compare


class UpdateProductView(generic.UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "prod/create.html"
    context_object_name = "form"
    success_url = reverse_lazy("product:liste")

    def get_context_data(self, **kwargs):
        product = super().get_context_data()
        print(product["form"])
        # categorie = product["name"].name
        # return categorie


class DeleteProductView(generic.DeleteView):
    model = Product
    template_name = "prod/delete.html"
    context_object_name = "product"
    success_url = reverse_lazy("myhome")

    def get_context_data(self, **kwargs):
        product = super().get_context_data()
        print(product)


class DeleteCategorieView(generic.DeleteView):
    model = Category
    template_name = "prod/delete.html"
    context_object_name = "product"
    success_url = reverse_lazy("myhome")


class UpdateVenteJour(generic.UpdateView):
    model = VenteJournaliere
    form_class = VentJournaliereform
    success_url = reverse_lazy("myhome")
    template_name = "prod/create.html"


def create_product(request):
    """
        - Boutique : qui sera recupéré, par le connecté
        - Categorie : recuperé ou créé
    """
    if request.method == "POST":
        product = request.POST.get("name").lower()
        cat = request.POST.get("category").lower()
        category = categori_maker(cat)
        quantity = request.POST.get("quantity")
        price = request.POST.get("price")
        unity = request.POST.get("unity")
        try:
            cate = category.products.all().get(name=product)
            # print("category", cat)
            if not cate:

                Product.objects.create(
                    category=category,
                    name=product,
                    unity=unity,
                    quantity=quantity,
                    price=price,
                )
                return redirect("product:liste")
            else:
                return HttpResponse("produit exist deja")
        except Exception as exept:
            # quantity = request.POST.get("quantity")
            # price = request.POST.get("price")
            # unity = request.POST.get("unity")
            Product.objects.create(
                category=category,
                name=product,
                unity=unity,
                quantity=quantity,
                price=price,
            )

            return redirect("product:liste")
            # return HttpResponseRedirect(request.path)
    else:
        form = ProductForm()
    return render(request, "prod/create.html", context={
        "form": form,
        "title": "Nouveau Produit"
        # "cats": categorie
    })


def categori_maker(categorie):
    cat, create = Category.objects.get_or_create(name=categorie)
    if create:
        return Category.objects.only("pk").get(name=cat)
    return Category.objects.only("pk").get(name=cat)


class CreateVenteJour(generic.CreateView):
    model = VenteJournaliere
    fields = (
        "command",
        "product",
        "quantitte",
    )
    template_name = "prod/create.html"
    success_url = reverse_lazy("myhome")


class DeleteVenteJour(generic.DeleteView):
    model = VenteJournaliere
    template_name = "prod/delete.html"
    context_object_name = "product"
    success_url = reverse_lazy("myhome")


def create_daylysold(requests):
    if requests.method == "POST":
        form = VentJournaliereform(requests.POST)
        product_pk = int(requests.POST.get("product"))
        product = Product.objects.only("price").get(pk=product_pk)
        if form.is_valid():
            form = form.save(commit=False)
            controle = new_hold_compare(form.quantity, product.quantity)
            # print(controle)
            if controle:
                if not form.price:
                    form.price = product.price
                    form.save()
                else:
                    form.save()
                return HttpResponseRedirect(requests.path)
        return HttpResponse("valeur superieur au stock")

    else:

        form = VentJournaliereform()

    return render(requests, "prod/create.html", context={
        "form": form,
        "title": "Vente Journalière"
        # "product": product
    })


def categorie_sup(request, pk):
    category = get_object_or_404(Category, pk=pk)
    produit = category.products.all()

    if request.method == "POST":
        category.delete()
        return redirect("myhome")
    return render(request, "prod/delete.html", context={"product": category, "produit": produit})


def box_delete_modal(request, pk):
    product = get_object_or_404(Product, pk=pk)

    obj_title = "le produit"
    return render(request, 'global/delete_modal.html', {"object": product, "suppress_object": obj_title})


def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    ventejour = product.produit_vendu.all()
    invoice_item = product.supplier_invoice_item.all()
    client_item = product.client_invoice_item.all()
    if request.method == "POST":
        product.delete()
        return redirect("product:liste")

    return render(request,
                  "prod/delete.html",
                  context={
                      "object": product,
                      "ventejour": ventejour,
                      "invoice_item": invoice_item,
                      "client_item": client_item
                  })


def product_update(request, pk):
    if request.method == 'PUT':
        # Récupérer l'objet correspondant
        product = get_object_or_404(Product, pk=pk)

        try:
            # Charger les données envoyées dans la requête PUT
            data = json.loads(request.body)

            # Obtenir le champ et la valeur
            field = data.get('name')  # Nom du champ (product, quantity ou price)
            value = data.get('value')  # Nouvelle valeur
            print("field", field)
            print("value", value)

            # Vérification : Valider et mettre à jour uniquement les champs autorisés
            if field in ['name', 'quantity', 'price']:
                if field == 'name':
                    # Validation pour s'assurer que le prix est un nombre valide
                    value = value

                elif field == 'quantity':
                    # Validation pour s'assurer que quantity est un entier positif
                    if not value.isdigit() or int(value) < 0:
                        return JsonResponse({
                            'status': 'error',
                            'message': 'La quantité doit être un entier positif.'
                        }, status=400)
                    value = int(value)  # Convertir en entier

                elif field == 'price':
                    # Validation pour s'assurer que le prix est un nombre valide
                    try:
                        value = float(value)
                        if value < 0:
                            return JsonResponse({
                                'status': 'error',
                                'message': 'Le prix doit être un nombre positif.'
                            }, status=400)
                    except ValueError:
                        return JsonResponse({
                            'status': 'error',
                            'message': 'Prix invalide.'
                        }, status=400)

                # Mettre à jour le champ et sauvegarder
                setattr(product, field, value)
                product.save()

                return JsonResponse({
                    'status': 'success',
                    'message': f'Champ "{field}" mis à jour avec succès.',
                    'updated_value': value
                })

            else:
                # Champ non autorisé
                return JsonResponse({
                    'status': 'error',
                    'message': f'Le champ "{field}" ne peut pas être modifié.'
                }, status=400)

        except json.JSONDecodeError:
            # Erreur si les données JSON sont invalides
            return JsonResponse({
                'status': 'error',
                'message': 'Données JSON invalides.'
            }, status=400)

    # Méthode HTTP non autorisée
    return JsonResponse({
        'status': 'error',
        'message': 'Méthode non autorisée.'
    }, status=405)


# def create_stock(request, pk):
#     if request.method == "POST":
#         form = NewStockForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("product:liste")
#     else:
#         prod = Product.objects.only("name", "pk").get(pk=pk)
#         initial = {
#             "name": prod
#         }
#         form = NewStockForm(initial=initial)
#         context = {
#             "form": form
#         }
#     return render(request, "prod/create.html", context)
#

def product_autocomplete(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(name__icontains=query)[:10]  # Limite à 10 résultats
    data = [{'name': product.name, 'id': product.id} for product in products]
    return JsonResponse(data, safe=False)


class ListeProductView(generic.ListView):
    model = Product
    template_name = "prod/liste.html"
    context_object_name = "product"
    paginate_by = 10  # Nombre d'articles à charger par page

    def get_queryset(self):
        return Product.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ProductForm()
        return context


# Vue pour charger plus de produits
def load_more(request):
    product = Product.objects.all()
    pagination = Paginator(product, 1)
    page_number = request.GET.get("page", 1)
    page_obj = pagination.get_page(page_number)

    return render(request, "prod/partial/product_list.html", {"product": page_obj})


def liste_product_view(request):
    product = Product.objects.all()

    # Pagination
    paginator = Paginator(product, 100)  # 10 articles par page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    if request.htmx:  # Si la requête est faite par HTMX
        return render(request, 'prod/partial/product_list.html', {'product': page_obj})
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
    form = ProductForm()
    # Si ce n'est pas une requête HTMX, charge la page complète
    return render(request, 'prod/liste.html', {'product': page_obj, "form": form, "product_count":product})


# def list_commande(request):
#     commande = Command.objects.all()
#     form = CommandForm()
#     return render(request, "prod/command_handler.html", context={"form": form, "command": commande})
#
#
# def create_command(request):
#     # form = formset_factory(CommandForm,extra=10)
#     # user = Customer.objects.only("pk").get(pk=pk)
#     if request.method == "POST":
#         product = request.POST.get("product")
#         form = CommandForm(request.POST)
#         if form.is_valid():
#             item = form.save()
#             return render(request, "prod/partial/command_line.html", context={"form":form,"item":item})
#             # return HttpResponseRedirect(request.path)
#             # return HttpResponser("Bon de commande enregistrer")
#     else:
#         initial = {
#             # "customer": user,
#             "add_date": datetime.date.today()
#         }
#         form = CommandForm(initial=initial)
#     context = {
#         "form": form,
#         "title": "Bon de Commande"
#     }
#     return render(request, "prod/partial/create_command.html", context)

# def create_command(request, pk):
#     # form = formset_factory(CommandForm,extra=10)
#     user = Customer.objects.only("pk").get(pk=pk)
#     if request.method == "POST":
#         form = CommandForm(request.POST)
#
#         all_product = request.POST.get("product")
#         sold_day = request.POST.get("sold_day")
#         status = request.POST.get("status")
#         data = all_product, sold_day, status, user
#         command_product(all_product, sold_day, status, user)
#         # Product.objects.create(
#         #     customer="",
#         #     product="",
#         #     quantity="",
#         #     price="",
#         #     excecuted="",
#         #     add_date="",
#         # )
#     else:
#         initial = {
#             "customer": user,
#             "add_date": datetime.date.today()
#         }
#         form = CommandForm(initial=initial)
#     context = {
#         "form": form,
#         "title": "Bon de Commande"
#     }
#     return render(request, "prod/create_command.html", context)



    products = fake_prod_data()
    for product in products:
        # cat,_ = Category.objects.get_or_create(name=product.get("catégorie"))
        cat_id = product.get("catégorie")
        cat = fake_category(cat_id)
        prod = product.get("nom")
        quantit = product.get("quantité")
        unit = product.get("unité")
        prix = product.get("prix")
        date = product.get("date")
        try:
            product = Product.objects.get_or_create(
                category=cat,
                name=prod,
                quantity=quantit,
                unity=unit,
                price=prix,
                date=date,

            )
            print(product)
        except Exception as E:
            continue

# fake_product()

# class NewStockList(generic.ListView):
#     model = NewStock
#     template_name = "prod/liste.html"
#     context_object_name = "product"


# class NewStockCreate(generic.CreateView):
#     model = NewStock
#     form_class = NewStockForm
#     template_name = "prod/create.html"
#     success_url = reverse_lazy("product:liste")
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = "Nouveau produit en stock"
#
#         return context


# class NewStockDelete(generic.DeleteView):
#     model = NewStock
#     template_name = "prod/delete.html"
#     context_object_name = "product"
#     success_url = reverse_lazy("myhome")
#
# class ListeProductView(generic.ListView):
#     model = Product
#     template_name = "prod/liste.html"
#     context_object_name = "products"
#     paginate_by = 10
#
#     def get_queryset(self):
#         return Product.objects.all()
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["form"] = ProductForm()
#         return context
#
#     def render_to_response(self, context, **response_kwargs):
#         if self.request.htmx:
#             page = self.request.GET.get("page", 1)
#             paginator =Paginator(self.get_queryset(), self.paginate_by)
#             products = paginator.get_page(page)
#             html = render_to_string("prod/partials/product_list.html", {"products":products})
#             return  JsonResponse({"html":html, "has_net":products.has_next()}, status=200)
#         return super().render_to_response(context, **response_kwargs)
def daily_sales_view(request):
    today = timezone.now().date()
    sales = VenteJournaliere.objects.filter(add_date=today).select_related('product')
    
    total_revenue = sales.aggregate(total=Sum('totalprice'))['total'] or 0
    total_quantity = sales.aggregate(total=Sum('quantity'))['total'] or 0
    
    context = {
        'sales': sales,
        'today': today,
        'total_revenue': total_revenue,
        'total_quantity': total_quantity,
        'title': "Vente Journalière"
    }
    return render(request, "product/daily_sales.html", context)
