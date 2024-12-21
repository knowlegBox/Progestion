import datetime

from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from customers.models import Customer
from facture.models import MyInvoice
from transactions.form import VersementForm, SpendForm
from transactions.models import Versement, DailySpend


class SpendCreateView(generic.CreateView):
    model = DailySpend
    form_class = SpendForm
    template_name = "transactions/createtemp.html"
    success_url = reverse_lazy("transaction:liste_spend")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Enregistrer les dépenses journalieres"
        context["date"] = datetime.date.today()

        return context

    def get_initial(self):
        initial = super().get_initial()
        initial["date"] = datetime.date.today()
        return initial


class SpendListeView(generic.ListView):
    model = DailySpend
    template_name = "transactions/spendlist.html"
    context_object_name = "daylyspents"


class SpendDeleteView(generic.DeleteView):
    model = DailySpend
    template_name = "transactions/delete.html"
    success_url = reverse_lazy("transaction:liste_spend")
    context_object_name = "customer"


class CreateVersementView(generic.CreateView):
    model = Versement
    fields = (
        "user",
        "choice",
        "amount",
    )
    template_name = "transactions/create.html"
    success_url = reverse_lazy("customer:detail")


def versement_delete(request, pk):
    if request.method == "POST":
        instance_depot = Versement.objects.only("pk").get(pk=pk)
        try:
            user_pk = instance_depot.user.pk
            instance_depot.delete()
            return redirect("customer:detail", user_pk)
        except Exception as E:
            user_pk = instance_depot.supplier.pk
            instance_depot.delete()
            return redirect("supplier:supplier_detail", user_pk)
    else:
        product = Versement.objects.get(pk=pk)
    return render(request, "transactions/delete.html", context={"product": product})


# -------- Withdrall  -----------------


def facture_delete(request, pk):
    if request.method == "POST":
        instance_depot = MyInvoice.objects.get(pk=pk)
        user_pk = instance_depot.customer.pk
        instance_depot.delete()
        # return redirect("customer:detail", user_pk)
        reverse("customer:detail", user_pk)
    else:
        product = MyInvoice.objects.get(pk=pk)
    return render(request, "transactions/delete.html", context={"product": product})


def list_transaction(request):
    versement = Versement.objects.all()
    retrait = MyInvoice.objects.all()
    # solde = OperationDepotRetrait.objects.get()
    context = {
        "depots": versement,
        "retraits": retrait,
        #         "solde": solde
    }
    return render(request, "transactions/detail.html", context)


def create_depot(request, pk):
    if request.method == "POST":

        form = VersementForm(request.POST)
        user_id = int(request.POST.get("user"))
        if form.is_valid():
            form.save()
            return redirect("customer:detail", pk=user_id)
    else:
        user_pk = Customer.objects.only("pk").get(pk=pk)
        initial = {
            "user": user_pk,
            "recipient_type": "CUSTOMER"
        }
        form = VersementForm(initial=initial)

    return render(request, "transactions/create.html", context={"form": form, "title": "Client"})


def create_daylyspend(request):
    form = SpendForm()
    return render(request, "transactions/createtemp.html", context={"form": form})


# def make_spend():
#     data = fake_spend_date()
#     for i in data:
#         for key, value in i.items():
#             DailySpend.objects.create(
#                 name=i.get("name"),
#                 value=float(i.get("value")),
#                 observation=i.get("observation"),
#                 add_date=i.get("date"),
#             )


# make_spend()
