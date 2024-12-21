from django import forms

from customers.models import Customer
from product.models import Product, Category, VenteJournaliere


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        # fields = ("category",
        #           "name",
        #           # "image",
        #           "price",
        #           "unity",
        #           "quantity",
        #           "available",
        #           )
        fields = "__all__"

        widgets = {
            "category": forms.TextInput(attrs={"placeholder": "Catégorie", "class": "rounded-md w-60"}),

            "quantity": forms.TextInput(attrs={"style": "display:none",
                                               "placeholder": "Quantité", "class": "rounded-md  w-60"}),
            "unity": forms.Select(attrs={"placeholder": "Unité", "class": "rounded-md", "style": "width:210px;"}),
            "price": forms.NumberInput(attrs={"placeholder": "Prix ", "class": "rounded-md w-60"}),
            "name": forms.TextInput(attrs={"placeholder": "Produit", "class": "rounded-md w-60"})
        }
        labels = {
            "name": "",
            "quantity": "",
            "category": "",
            "unity": "",
            "price": "",
        }





class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = (
            "name",)


class VentJournaliereform(forms.ModelForm):
    class Meta:
        model = VenteJournaliere
        fields = (
            "product",
            "quantity",
            "price"
            #     "reste"
        )
        widgets = {
            # "product": forms.TextInput(),
            "product": forms.Select(attrs={"placeholder": "Produit", "class": "rounded-md", "style": "width:210px;",
                                           "list": "product_items"}),
            "quantity": forms.NumberInput(attrs={"placeholder": "Quantité", "class": "rounded-md w-60"}),
            "price": forms.NumberInput(attrs={"placeholder": "Prix", "class": "rounded-md w-60"}),
        }
        labels = {
            "product": "",
            "quantity": "",
            "price": ""
        }
