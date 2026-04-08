import json

from django.db.models import Sum, FloatField, F
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic

from product.models import Product
from transactions.form import VersementForm
from transactions.models import Versement
from .form import SupplierForm, SupplierInvoiceItemsForm
from .models import Supplier, SupplierInvoiceItems, SupplierInvoices


class SupplierInvoiceItemsList(generic.ListView):
    model = SupplierInvoiceItems
    template_name = "prod/liste.html"
    context_object_name = "product"


class SupplierInvoiceItemsCreate(generic.CreateView):
    model = SupplierInvoiceItems
    form_class = SupplierInvoiceItemsForm
    template_name = "prod/create.html"
    success_url = reverse_lazy("product:liste")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Nouveau produit en stock"

        return context


class SupplierInvoiceItemsDelete(generic.DeleteView):
    model = SupplierInvoiceItems
    template_name = "prod/delete.html"
    context_object_name = "product"
    success_url = reverse_lazy("myhome")


def create_stock(request, pk):
    if request.method == "POST":
        form = SupplierInvoiceItemsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("product:liste")
    else:
        prod = Product.objects.only("name", "pk").get(pk=pk)
        initial = {
            "name": prod
        }
        form = SupplierInvoiceItemsForm(initial=initial)
    context = {
        "form": form
    }
    return render(request, "prod/create.html", context)


class SupplierInvoiceItemsList(generic.ListView):
    model = SupplierInvoiceItems
    template_name = "prod/liste.html"
    context_object_name = "product"


class SupplierInvoiceItemsCreate(generic.CreateView):
    model = SupplierInvoiceItems
    form_class = SupplierInvoiceItemsForm
    template_name = "prod/create.html"
    success_url = reverse_lazy("product:liste")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Nouveau produit en stock"

        return context


class SupplierInvoiceItemsDelete(generic.DeleteView):
    model = SupplierInvoiceItems
    template_name = "prod/delete.html"
    context_object_name = "product"
    success_url = reverse_lazy("myhome")


def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'suppliers/supplier_list.html', {'suppliers': suppliers})


def supplier_detail(request, supplier_id):
    supplier = Supplier.objects.only("pk", "name").get(pk=supplier_id)
    versmt = Versement.objects.filter(supplier=supplier)
    facture = SupplierInvoices.objects.filter(supplier=supplier)

    solde = supplier_account(supplier_id)
    supplier.solde = solde[2]
    supplier.save()

    context = {
        "supplier": supplier,
        "versmt": versmt,
        "facture": facture,
        "total_fact": solde[1],
        "total_versmt": solde[0],
        "reste": solde[2]
    }
    return render(request, "suppliers/detail.html", context)


def supplier_account(pk):
    versmt = Versement.objects.only("pk", "amount").filter(supplier=pk)
    facture = SupplierInvoices.objects.only("supplier", "total_price").filter(supplier=pk)
    total_versmt = versmt.aggregate(total=Sum("amount"))["total"] or 0
    total_facture = facture.aggregate(total=Sum("total_price"))["total"] or 0
    reste = total_facture - total_versmt
    return total_versmt, total_facture, reste


def supplier_create(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supplier:supplier_list')
    else:
        form = SupplierForm()
    return render(request, 'suppliers/supplier_form.html', {'form': form})


def supplier_update(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('supplier:supplier_list')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'suppliers/supplier_form.html', {'form': form})


def supplier_delete(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)
    if request.method == 'POST':
        supplier.delete()
        return redirect('supplier:supplier_list')
    return render(request, 'prod/delete.html', {'object': supplier})


def create_depot(request, pk):
    user_pk = Supplier.objects.only("pk", 'name').get(pk=pk)
    if request.method == "POST":
        form = VersementForm(request.POST)
        supplier_id = int(request.POST.get("supplier"))
        if form.is_valid():
            form.save()
            return redirect("supplier:supplier_detail", user_pk.pk)
            # return redirect("supplier:supplier_detail", pk=user_pk.pk)
    else:
        # user_pk = Supplier.objects.only("pk").get(pk=pk)
        initial = {
            "supplier": user_pk,
            "recipient_type": "SUPPLIER"
        }
        form = VersementForm(initial=initial)

    return render(request, "suppliers/create.html", context={"form": form, "title": "Fournisseur"})


# ---------------------- invoice -----------------------
def invoice_home(request, pk):
    last_invoice = create_new_invoice(pk)
    supplier = Supplier.objects.only("name").get(pk=pk)
    form = SupplierInvoiceItemsForm()
    all_product = Product.objects.only("pk", "name", "price").all()[:50]
    return render(request, "invoice/invoicehome.html", context={
        "form": form,
        "products": all_product,
        "info": last_invoice,
        "supplier": supplier,
    })


# def create_new_invoice(pk):
#     try:
#         supplier = Supplier.objects.only("name", "pk").get(pk=pk)
#         # Nous ne vérifions plus si last_invoice.invoice.all() existe
#         return SupplierInvoices.objects.create(supplier=supplier)
#
#     except Supplier.DoesNotExist:
#         # Gérer spécifiquement le cas où le fournisseur n'existe pas
#         raise ValueError(f"Supplier with pk {pk} does not exist")
#
#     except Exception as e:
#         # Loggez l'erreur pour le débogage
#         import logging
#         logging.error(f"Error creating new invoice: {str(e)}")
#         raise  # Relancer l'exception pour la gestion en amont


#
#
def add_to_invoice(request, pk):
    product = Product.objects.get(id=pk)
    context = {
        'product': product,
    }
    line_item_html = render_to_string('invoice/partial/invoice_line_item.html', context)
    return HttpResponse(line_item_html)


def invoice_detail(request, invoice_id):
    invoice = get_object_or_404(SupplierInvoices, id=invoice_id)
    invoice_lines = invoice.invoice.all()
    if request.method == "GET":
        total = invoice.invoice.aggregate(total=Sum(F('quantity') * F('price'), output_field=FloatField()))['total'] or 0
        invoice.total_price = total
        invoice.save()

        return render(request, 'invoice/invoice_detail.html', {
            'invoice_detail': invoice_lines,
            'total': total,
            'give_inv': invoice
        })


def create_invoice(request):
    """
    -creer un produit s'il n'exist pas
      - cre
    """
    if request.method == 'POST':
        last_invoice_id = SupplierInvoices.get_last_id()
        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                product_id = int(key.split('_')[1])
                quantity = int(value)
                price_key = f'price_{product_id}'
                price = float(request.POST.get(price_key, ))

                if quantity > 0:
                    product = get_object_or_404(Product, pk=product_id)
                    try:
                        price = float(request.POST.get(price_key))
                    except Exception as e:
                        price = product.price

                    SupplierInvoiceItems.objects.create(
                        invoice=last_invoice_id,
                        product=product,
                        quantity=quantity,
                        price=price,
                        add_date=timezone.now()
                    )
        return redirect('supplier:invoice_detail', invoice_id=last_invoice_id.id)
    # return redirect("suppl")
    return redirect('facture:product_list')


def delete_invoice_item(request, pk):
    item = get_object_or_404(SupplierInvoiceItems, pk=pk)
    invoice_pk = item.invoice
    if item:
        item.delete()
        return redirect("supplier:invoice_detail", invoice_id=invoice_pk.pk)
    return HttpResponse("Produit inexistant")


def delete_invoice(request, pk):
    my_invoice = get_object_or_404(SupplierInvoices, pk=pk)
    user_pk = my_invoice.supplier
    if my_invoice:
        my_invoice.delete()
        # return reverse("customer:detail", user_pk.pk)
        a = supplier_detail(request, user_pk.pk)
        return a
    return HttpResponse("Facture supprimer avec succès")


# def create_invoice(request):
#     if request.method != 'POST':
#         return redirect('facture:product_list')
#
#     last_invoice = MyInvoice.get_last_id()
#
#     items_to_create = []
#
#     for key, value in request.POST.items():
#         if not key.startswith('quantity_'):
#             continue
#
#         product_id = int(key.split('_')[1])
#         quantity = int(value)
#
#         if quantity <= 0:
#             continue
#
#         # product = get_object_or_404(Product, pk=product_id)
#         product, _ = Product.objects.get_or_create(pk=product_id)
#         print("create_invoice product",product)
#
#         price_key = f'price_{product_id}'
#
#         try:
#             price = float(request.POST.get(price_key, product.price))
#
#         except ValueError:
#             price = product.price
#
#         items_to_create.append(
#             SupplierInvoiceItems(
#                 invoice=last_invoice,
#                 product=product,
#                 quantity=quantity,
#                 price=price,
#                 add_date =timezone.now()
#             )
#         )
#
#     with transaction.atomic():
#         SupplierInvoiceItems.objects.bulk_create(items_to_create)
#
#     return redirect('facture:invoice_detail', invoice_id=last_invoice.id)


def create_new_invoice(pk):
    try:
        supplier = Supplier.objects.only("name", "pk").get(pk=pk)
        last_invoice = SupplierInvoices.get_last_id()
        all_invoice = last_invoice.invoice.all()
        if all_invoice:
            info = SupplierInvoices.objects.create(
                supplier=supplier
            )
            return info
        return supplier
    except Exception as E:
        supplier = Supplier.objects.only("name", "pk").get(pk=pk)
        info = SupplierInvoices.objects.create(
            supplier=supplier
        )
        return info


