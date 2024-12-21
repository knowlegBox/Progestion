from django.db import models

from facture.models import MyInvoice, MyInvoiceItem


# Create your models here.

class Seller(models.Model):
    # store = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="shop_seller")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    number1 = models.CharField(max_length=20, blank=True)
    number2 = models.CharField(max_length=20, blank=True)
    solde = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class SellerInvoices(MyInvoice):
    seller = models.ForeignKey(Seller, on_delete=models.Model, verbose_name="seller_invoice")


class SellerInvoiceItem(MyInvoiceItem):
    pass
    # seller_item = models.ForeignKey(SellerInvoices, on_delete=models.Model, verbose_name="invoice_item")
