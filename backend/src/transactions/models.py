from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.shortcuts import redirect
from django.utils import timezone

from customers.models import Customer
from supplier.models import Supplier

OPERATION_TYPE = (
    ("Espèce", "Espèce"),
    ("Produit", "Produit")
)

RECIPIENT_TYPES = [
    ('SUPPLIER', 'Fournisseur'),
    ('CUSTOMER', 'Client'),
]


class DailySpend(models.Model):
    name = models.CharField(max_length=100, verbose_name="Désignation")
    value = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Valeur")
    observation = models.TextField(blank=True)
    # date = models.DateTimeField(auto_now_add=True)
    add_date = models.DateTimeField(default=timezone.now, blank=True, null=True, verbose_name="Date")


class Versement(models.Model):
    recipient_type = models.CharField(max_length=8, choices=RECIPIENT_TYPES, db_index=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True,)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True, related_name="client_versmt")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    # supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name="supplier_vers", null=True,
    # blank=True ) user = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="client_vers",
    # null=True, blank=True) # choice = models.CharField(choices=OPERATION_TYPE, max_length=10, blank=True) amount =
    # models.IntegerField() date = models.DateTimeField(auto_now_add=True) add_date = models.DateTimeField(
    # blank=True, null=True, verbose_name="Date")

    class Meta:
        ordering = ("-date",)

    def clean(self):
        if self.recipient_type == 'SUPPLIER' and not self.supplier:
            raise ValidationError("Un fournisseur doit être spécifié pour ce type de versement.")
        if self.recipient_type == 'CUSTOMER' and not self.user:
            raise ValidationError("Un client doit être spécifié pour ce type de versement.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.amount}"

    def get_absolute_url(self):
        return redirect("customer:detail", args=self.user)

# class Facture(models.Model):
#     user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="user_withdrawal")
#     value = models.IntegerField(verbose_name="Valeur", null=True, blank=True)
#     # product = models.CharField(max_length=50, blank=True, verbose_name="Produit")
#     # product = models.ForeignKey(Product, on_delete=models.CASCADE())
#     date = models.DateTimeField(auto_now_add=True)
#
#     # add_date = models.DateTimeField(blank=True, null=True, verbose_name="Date")
#
#     def get_absolute_url(self):
#         return reverse("customer:detail", args=self.user)
#
#     def __str__(self):
#         return f"{self.value}"


# class OperationDepotRetrait(models.Model):
#     """
#     affichage du solde du client c'est ici qu'on deduira les montants retirés et ajoutéra les montants versés
#     """
#     user = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     versement = models.IntegerField(default=0)  # recevra la somme de tous les dépot effectués par ce client
#     facture = models.IntegerField(default=0)  # recevra la somme de tous les retrait effectués par ce client
#     reste = models.IntegerField(default=0)  # ce qui sera affiché dans pour donné le reste
#     date = models.DateTimeField(auto_now_add=True)


# @receiver(pre_delete, sender=Versement)
# def del_versmt(signal, instance, **kwargs):
#     user = instance.user
#     value = instance.amount
#     #     user_pk = get_object_or_404(Customer, pk=user.pk)
#     versmt = OperationDepotRetrait.objects.only("pk").get(user=user.pk)
#
#     if versmt.versement < 0:
#         versmt.versement = 0
# @receiver(post_save,sender=Versement)
# def reste_value(signal, instance, **kwargs):
#     transaction = OperationDepotRetrait.objects.get(user=instance.user.pk)
#     transaction.versement += instance.amount
#     transaction.reste = transaction.facture - transaction.versement
#     if not transaction.reste:
#         transaction.versement = 0
#         transaction.facture =0
#
#     transaction.save()
