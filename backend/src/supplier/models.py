from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone

from product.models import Product
from zimpot.utilitaire import invoice_number


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=255)
    solde = models.IntegerField(default=0)

    def __str__(self):
        return self.name


# class NewStock(models.Model):
#     invoice = models.ForeignKey("facture.MyInvoice", on_delete=models.CASCADE, verbose_name="inv_stock")
#     product = models.ForeignKey("product.Product", on_delete=models.CASCADE, verbose_name="Produits")
#     quantity = models.PositiveIntegerField(verbose_name="Quantité")
#     price = models.DecimalField(verbose_name="Prix", max_digits=10, decimal_places=2)
#     add_date = models.DateTimeField(default=timezone.now, verbose_name="Date")
#
#     def __str__(self):
#         return f"{self.name} : {self.quantity}"
#
#     def total_cost(self):
#         return


class SupplierInvoices(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="supplier_invoice")
    date = models.DateField(auto_now_add=True)
    number = models.CharField(max_length=20, blank=True)  # numero du bon de commande
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        ordering = ("-date", "-number")

    def __str__(self):
        return f"{self.number}"

    def save(self, *args, **kwargs):
        if not self.number:
            try:
                nombre = self.get_last_id()
                nombre_01 = nombre.number
                numero = invoice_number(nombre_01)
                self.number = numero
            except Exception as e:
                numero = invoice_number()
                self.number = numero

        super().save(*args, **kwargs)

    @classmethod
    def get_last_id(cls):
        return cls.objects.latest("id")


class SupplierInvoiceItems(models.Model):
    invoice = models.ForeignKey(SupplierInvoices, on_delete=models.CASCADE, related_name="invoice")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="supplier_invoice_item")
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    add_date = models.DateTimeField(default=timezone.now, verbose_name="Date")

    def save(self, *args, **kwargs):
        if not self.price:
            price = Product.objects.only("price").get(pk=self.product.pk)
            self.price = price.price
        super().save(*args, **kwargs)

    def sub_total_price(self):
        return self.price * self.quantity


@receiver(post_save, sender=SupplierInvoiceItems)
def product_update(sender, instance, **kwargs):
    new_entry = instance.product
    new_quantity = instance.quantity
    prod = Product.objects.only("name", "quantity").get(name=new_entry)
    prod.quantity += new_quantity
    prod.save()

# @receiver(post_save, sender=SupplierInvoices)
# def new_stok_add(sender, instance , **kwargs):
#     invoice = instance

