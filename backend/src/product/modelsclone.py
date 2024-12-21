from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models, transaction
# from django.db.models import Q
from django.urls import reverse
from django.utils.text import slugify

UNITY = (

    ("botte", "botte"),
    ("barre", "barre"),
    ("tonne", "tonne"),
    ("paquet", "paquet"),
    ("boite", "boite"),
    ("mettre", "m"),
    ("feuille", "feuille"),
    (None, "Unité")
)


class Category(models.Model):
    name = models.CharField(max_length=200,unique=True, db_index=True)
    date = models.DateTimeField(auto_now_add=True)
    # slug = models.SlugField(max_length=200, unique=True, blank=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"

    def __str__(self):
        return self.name

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.name)
    #     super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("shop:product_list_by_category",
                       args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", verbose_name="Catégorie")
    name = models.CharField(max_length=200, db_index=True, verbose_name="Produit")
    quantity = models.PositiveIntegerField(
        default=0,
        verbose_name="Quantité"

    )  # il contient la quantité entrée, ensuite on  le mais a jour avec la valeur qui entre
    unity = models.CharField(choices=UNITY, verbose_name="Unité", max_length=15)
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Prix")

    # updated = models.DateTimeField(auto_now=True)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    # slug = models.SlugField(max_length=200, db_index=True, blank=True)
    # image = models.ImageField(upload_to="product/%Y/%m/%d", blank=True)
    # description = models.TextField(blank=True)

    class Meta:
        ordering = ("name",)
        # index_together = (("id", "slug"),)
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse("shop:product_detail",
    #                    kwargs={"slug": self.slug, "id": self.pk})

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.name)
    #     super().save(*args, **kwargs)


class NewStock(models.Model):
    name = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Produits")
    quantity = models.PositiveIntegerField(verbose_name="Quantité")
    date = models.DateTimeField(auto_now=True, verbose_name="Date")

    # name = models.CharField(max_length=50, verbose_name="Produits")

    def __str__(self):
        return f"{self.name} : {self.quantity}"


# class AvailableStock(models.Model):
#     # name = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="Produit")
#     name = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Produit")
#     reste = models.PositiveIntegerField(default=0, verbose_name="Reste")
#     last_value = models.PositiveIntegerField(default=0, verbose_name="Valeur Precedente")
#     available = models.BooleanField(default=True, verbose_name="Disponibilité")
#     created = models.DateTimeField(auto_now_add=True, verbose_name="Créer le")


class VenteJournaliere(models.Model):
    # product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="produit_vendu")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="produit_vendu")
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    quantity = models.PositiveIntegerField(verbose_name="Quantité")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date")
    stock = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        ordering = ["-date"]
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'date'],  # Champs à considérer pour la contrainte d'unicité
                name="unique_product_per_day"  # Nom de la contrainte d'unicité
            )
        ]


@receiver(post_save, sender=NewStock)
def product_update(sender, instance, **kwargs):
    new_entry = instance.name
    new_quantity = instance.quantity
    prod = Product.objects.only("name", "quantity").get(name=new_entry)
    prod.quantity += new_quantity
    prod.save()

@receiver(post_save, sender=VenteJournaliere)
def dayly_sold(sender, instance, **kwargs):
    produit = Product.objects.only("name", "quantity").get(name=instance.product)

    # Utilisation d'une transaction pour garantir l'intégrité des données
    with transaction.atomic():
        # Désactivation temporaire du signal post_save pour les objets Product et AvailableStock
        post_save.disconnect(dayly_sold, sender=VenteJournaliere)

        # available, create = AvailableStock.objects.get_or_create(name=produit)

        last_value = produit.quantity  # quantité de produit dans la table product
        reste = last_value - instance.quantity  # reste dans la table available_stock
        # available.reste = reste  # reste à stocker dans available_stock
        # available.last_value = last_value  # la valeur précédente dont à déduit la valeur de VenteJournaliere
        produit.quantity = reste  # la valeur reste mettra à jour celui contenu dans produit
        instance.stock = reste

        # Enregistrement des objets mis à jour
        # available.save()
        produit.save()
        instance.save()

        # Rétablissement du signal post_save pour les objets Product et AvailableStock
        post_save.connect(dayly_sold, sender=VenteJournaliere)
