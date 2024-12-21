from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models

from supplier.models import Supplier
from zimpot.utilitaire import invoice_number

from customers.models import Customer
from product.models import Product, VenteJournaliere

STATE = (
    ("En attente", "En attente"),
    ("Livré", "Livré")
)
RECIPIENT_TYPES = [
    ('buy', 'Achat'),
    ('sold', 'Vente'),
]


class MyInvoice(models.Model):
    recipient_type = models.CharField(max_length=8, choices=RECIPIENT_TYPES)
    # supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="sup_invoice", blank=True,
    # null=True,)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="custom_invoice", blank=True, null=True,)
    date = models.DateField(auto_now_add=True)
    number = models.CharField(max_length=15, blank=True)  # numero du bon de commande
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


class MyInvoiceItem(models.Model):
    invoice = models.ForeignKey(MyInvoice, on_delete=models.CASCADE, related_name="invoice")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="client_invoice_item")
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)

    # total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)

    def save(self, *args, **kwargs):
        if not self.price:
            price = Product.objects.only("price").get(pk=self.product.pk)
            self.price = price.price
        super().save(*args, **kwargs)

    def sub_total_price(self):
        return self.price * self.quantity


@receiver(post_save, sender=MyInvoice)
def my_invoice_post_operation(signal, instance, **kwargs):
    invoice_item = instance.invoice.all()
    print("invoice_item", invoice_item)
    for item in invoice_item:
        # print( "item_pk",item.pk)
        # print("invoice_item", item.product.name, item.product.pk, item.quantity, item.price)
        dayly_solde = VenteJournaliere.objects.create(command =item ,    
                                                        product=item.product,
                                                      price=item.price,
                                                      quantity=item.quantity, )
        # print("dayly_solde:",dayly_solde)
