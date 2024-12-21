from django.db.models import Sum, F, FloatField
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from customers.form import CustomerForm
from customers.models import Customer
from facture.models import MyInvoice
from transactions.models import Versement


class CreateCustomerView(generic.CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = "customers/create.html"
    success_url = reverse_lazy("customer:home")


class ListeCustomerView(generic.ListView):
    model = Customer
    context_object_name = "custom"
    template_name = "customers/home.html"


class DeleteCustomerView(generic.DeleteView):
    model = Customer
    template_name = "customers/delete.html"
    success_url = reverse_lazy("customer:home")
    context_object_name = "customer"


class UpdateCustomerView(generic.UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = "customers/create.html"
    success_url = "customer:home"


def list_customer(request):
    model = Customer
    context = {"custom": ""}
    return render(request, "customers/home.html", context)


def customer_detail(request, pk):
    customer = Customer.objects.only("pk", "name", "prenom", "solde").get(pk=pk)
    versmt = Versement.objects.filter(user=customer)
    facture = MyInvoice.objects.filter(customer=customer)

    solde = customer_account(pk)
    customer.solde = solde[2]
    print(solde[2])
    customer.save()

    context = {
        "customer": customer,
        "versmt": versmt,
        "facture": facture,
        "total_fact": solde[1],
        "total_versmt": solde[0],
        "reste": solde[2]
    }
    return render(request, "customers/detail.html", context)


def customer_account(pk):
    versmt = Versement.objects.only("pk", "amount").filter(user=pk)
    facture = MyInvoice.objects.only("customer", "total_price").filter(customer=pk)
    total_versmt = versmt.aggregate(total=Sum("amount"))["total"] or 0
    total_facture = facture.aggregate(total=Sum("total_price"))["total"] or 0
    reste = total_facture - total_versmt
    return total_versmt, total_facture, reste
