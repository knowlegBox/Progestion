from django.db import models


class Entreprise(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom Entreprise")
    rc = models.CharField(max_length=20, verbose_name="N°Registre Commerce")
    nc = models.CharField(max_length=20, verbose_name="N° Compte Contribuable")

    def __str__(self):
        return self.name


# Create your models here.
class Impots(models.Model):
    designation = models.CharField(max_length=50, verbose_name="Produit")
    prix = models.DecimalField(max_digits=9, decimal_places=2, default=0.0)
    nom_entr = models.ForeignKey(Entreprise, on_delete=models.CASCADE)
    valeur_ach = models.IntegerField(verbose_name="Valeur achat")
    valeur_impot = models.IntegerField(verbose_name="Valeur impot", blank=True)
    date_achat = models.DateField(verbose_name="Date Achat")
    # slug = models.SlugField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    add_date = models.DateTimeField(blank=True, null=True, verbose_name="Date")

    def __str__(self):
        return self.designation
