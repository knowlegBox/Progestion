from datetime import datetime

from django.db.models import Sum, F, FloatField
from django.http import HttpResponse, QueryDict
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views import generic

from customers import views
from customers.models import Customer
from facture.form import MyInvoiceItemForm
from facture.models import MyInvoice, MyInvoiceItem
from product.models import Product
from supplier.models import SupplierInvoices


class InvoiceList(generic.ListView):
    model = MyInvoice
    context_object_name = "invoices"
    template_name = "facture/invoice_list.html"


class InvoiceDeleteView(generic.DeleteView):
    model = MyInvoice
    template_name = "prod/delete.html"
    context_object_name = "product"
    success_url = reverse_lazy("facture:invoice_list")


def delete_invoice(request, pk):
    my_invoice = get_object_or_404(MyInvoice, pk=pk)
    user_pk = my_invoice.customer
    if my_invoice:
        my_invoice.delete()
        # return reverse("customer:detail", user_pk.pk)
        a = views.customer_detail(request, user_pk.pk)
        return a
    return HttpResponse("Facture supprimer avec succès")


def delete_invoice_item(request, pk):
    item = get_object_or_404(MyInvoiceItem, pk=pk)
    invoice_pk = item.invoice
    if item:
        item.delete()
        return redirect("facture:invoice_detail", invoice_id=invoice_pk.pk)
    return HttpResponse("Produit inexistant")


def invoice_item_edite(request, pk):
    context = {}
    item = get_object_or_404(MyInvoiceItem, pk=pk)
    print("invoice_item_edite", item)
    if request.method == "POST":
        form = MyInvoiceItemForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("facture:invoice_detail", pk=item.invoice.pk)
    else:
        item = get_object_or_404(MyInvoiceItem, pk=pk)
        form = MyInvoiceItemForm(instance=item)
        context = {
            "form": form
        }
    return render(request, "facture/partial/invoice_item_edite.html", context)


def create_invoice(request):
    if request.method == 'POST':
        last_invoice_id = MyInvoice.get_last_id()

        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                product_id = int(key.split('_')[1])
                quantity = int(value)
                price_key = f'price_{product_id}'
                # price = float(request.POST.get(price_key, ))

                if quantity > 0:
                    product = get_object_or_404(Product, pk=product_id)
                    try:
                        price = float(request.POST.get(price_key))
                    except Exception as e:
                        price = product.price

                    MyInvoiceItem.objects.create(
                        invoice=last_invoice_id,
                        product=product,
                        quantity=quantity,
                        price=price
                    )
        return redirect('facture:invoice_detail', invoice_id=last_invoice_id.id)
    return redirect('facture:product_list')


def create_new_invoice(pk):
    try:
        user = Customer.objects.only("name", "prenom", "pk").get(pk=pk)
        last_invoice = MyInvoice.get_last_id()
        all_invoice = last_invoice.invoice.all()
        if all_invoice:
            info = MyInvoice.objects.create(
                customer=user
            )
            return info
        return user
    except Exception as E:
        user = Customer.objects.only("name", "prenom", "pk").get(pk=pk)
        info = MyInvoice.objects.create(
            customer=user
        )
        return info


def add_to_invoice(request, pk):
    product = Product.objects.get(id=pk)
    context = {
        'product': product,
    }
    line_item_html = render_to_string('facture/partial/invoice_line_item.html', context)
    return HttpResponse(line_item_html)


def invoice_detail(request, invoice_id):
    invoice = get_object_or_404(MyInvoice, id=invoice_id)
    invoice_lines = invoice.invoice.all()
    if request.method == "GET":
        total = invoice.invoice.aggregate(total=Sum(F('quantity') * F('price'), output_field=FloatField()))['total']
        invoice.total_price = total
        invoice.save()

        return render(request, 'facture/invoice_detail.html', {
            'invoice_detail': invoice_lines,
            'total': total,
            'give_inv': invoice
        })


def invoice_home(request, pk):
    last_invoice = create_new_invoice(pk)
    user = Customer.objects.only("name", "prenom").get(pk=pk)
    form = MyInvoiceItemForm()
    all_product = Product.objects.only("pk", "name", "price").all()[:50]
    return render(request, "facture/invoicehome.html", context={
        "form": form,
        "products": all_product,
        "info": last_invoice,
        "user": user,
    })


def invoice_liste(request):
    client = MyInvoice.objects.all()
    supplier =SupplierInvoices.objects.all()
    print(supplier)
    return render(request, "facture/invoice_list.html", {"client": client, "supplier":supplier})
