from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=50, blank=True, verbose_name="Nom")
    prenom = models.CharField(max_length=100, blank=True, verbose_name="Prenoms")
    localisation = models.CharField(max_length=50, blank=True, verbose_name="Localisation")
    numero = models.CharField(max_length=15, blank=True, verbose_name="Numero")
    solde = models.IntegerField(default=0)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} {self.prenom}"
