import datetime

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import models, transaction
from django.urls import reverse
from django.utils import timezone

UNITY = (
    ("barre", "barre"),
    ("botte", "botte"),
    ("boite", "boite"),
    ("carton", "carton"),
    ("feuille", "feuille"),
    ("mettre", "m"),
    ("paquet", "paquet"),
    ("tonne", "tonne"),
    (None, "Unité")
)

STATE = (
    ("En attente", "En attente"),
    ("Livré", "Livré")
)


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True, db_index=True)
    image = models.ImageField(upload_to="categorie/", blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("shop:product_list_by_category",
                       args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", verbose_name="Catégorie",
                                 null=True, blank=True)
    name = models.CharField(max_length=200, unique=True, db_index=True, verbose_name="Produit")
    quantity = models.PositiveIntegerField(verbose_name="Quantité",
                                           default=0)  # il contient la quantité entrée, ensuite on  le mais a jour avec la valeur qui entre
    unity = models.CharField(choices=UNITY, verbose_name="Unité", max_length=15)
    price = models.IntegerField(verbose_name="Prix", default=0)
    # price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix", default=0)
    date = models.DateTimeField(auto_now=True, verbose_name="Date")

    class Meta:
        ordering = ("-date", "name")

        # index_together = (("id", "slug"),)
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return self.pk

    def quantity_value(self):
        return self.price * self.quantity

# class NewStock(models.Model):
#     name = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Produits")
#     quantity = models.PositiveIntegerField(verbose_name="Quantité")
#     price = models.DecimalField(verbose_name="Prix", max_digits=10, decimal_places=2)
#     add_date = models.DateTimeField(default=timezone.now, verbose_name="Date")

#     def __str__(self):
#         return f"{self.name} : {self.quantity}"


class VenteJournaliere(models.Model):
    command = models.ForeignKey("facture.MyInvoiceItem", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="produit_vendu")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Prix", blank=True, null=True)
    quantity = models.DecimalField(verbose_name="Quantité", max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date modif")
    add_date = models.DateField(default=timezone.now, verbose_name="Date")
    totalprice = models.IntegerField(db_index=True, null=True, blank=True)

    class Meta:
        ordering = ["-date"]
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'date'],  # Champs à considérer pour la contrainte d'unicité
                name="unique_product_per_day"  # Nom de la contrainte d'unicité
            )
        ]

    def __str__(self):
        return f'{self.product.name}'

    def save(self, *args, **kwargs):
        if not self.totalprice:
            self.totalprice = self.price * self.quantity
        super().save(*args, **kwargs)


@receiver(post_save, sender=VenteJournaliere)
def daylisold(signal, instance, **kwargs):
    product_instance = instance.product
    prod = Product.objects.get(pk=product_instance.pk)
    prod.quantity -= instance.quantity
    prod.save()

# @receiver(post_save, sender=NewStock)
# def product_update(sender, instance, **kwargs):
#     new_entry = instance.name
#     new_quantity = instance.quantity
#     prod = Product.objects.only("name", "quantity").get(name=new_entry)
#     prod.quantity += new_quantity
#     prod.save()


# @receiver(post_delete, sender=VenteJournaliere)
# def daylysold_delete(sender, instance, **kwargs):
#     quantiy = instance.quantity
#     product_pk = instance.product.pk
#     product = Product.objects.only("quantity").get(pk=product_pk)
#     product.quantity += quantiy
#     product.save()

# @receiver(post_save, sender=VenteJournaliere)
# def dayly_sold(sender, instance, **kwargs):
#     produit = Product.objects.only("name", "quantity").get(name=instance.product)
#
#     # Utilisation d'une transaction pour garantir l'intégrité des données
#     with transaction.atomic():
#         # Désactivation temporaire du signal post_save pour les objets Product et AvailableStock
#         post_save.disconnect(dayly_sold, sender=VenteJournaliere)
#
#         last_value = produit.quantity  # quantité de produit dans la table product
#         reste = last_value - instance.quantity  # reste dans la table available_stock
#         produit.quantity = reste  # la valeur reste mettra à jour celui contenu dans produit
#         instance.stock = reste
#
#         # Enregistrement des objets mis à jour
#         produit.save()
#         instance.save()
#
#         # Rétablissement du signal post_save pour les objets Product et AvailableStock
#         post_save.connect(dayly_sold, sender=VenteJournaliere)
