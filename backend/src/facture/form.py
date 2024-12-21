from django import forms

from django import forms

from facture.models import MyInvoiceItem, MyInvoice


class MyInvoiceItemForm(forms.ModelForm):
    class Meta:
        model = MyInvoiceItem
        fields = ["invoice",
                  "product",
                  "quantity",
                  "price"]
        widgets = {
            "invoice": forms.Select(attrs={"class": "rounded-md", "sytle": "width:100px;", "style": "display:none;"}, ),
            "product": forms.Select(attrs={"class": "rounded-md", "sytle": "width:200px;"}, ),
            "quantity": forms.NumberInput(attrs={"placeholder": "Qunatité", "class": "rounded-md w-36"}),
            "price": forms.NumberInput(attrs={"placeholder": "Prix", "class": "rounded-md w-36"})
        }
        labels = {
            "invoice": "",
            "product": "",
            "quantity": "",
            "price": ""
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields["invoice"].disabled = True
        # self.fields["product"].disabled = True


class MyInvoiceForm(forms.ModelForm):
    class Meta:
        model = MyInvoice
        fields = ("customer",
                  "recipient_type",
                  # "supplier",
                  )

# class CommandeForm(forms.ModelForm):
#     class Meta:
#         model = Commande
#         fields = (
#             "customer",
#             "excecuted",
#         )
#
#
# class LigneCommandeForm(forms.ModelForm):
#     class Meta:
#         model=LigneCommande
#         fields = (
#             "produit",
#             "quantity",
#             "price",
#         )

# class CommandForm(forms.ModelForm):
#     class Meta:
#         model = Command
#         fields = [
#             "customer",
#             "product",
#             "quantity",
#             "price",
#             "add_date",
#             "excecuted",
#
#         ]
#
#         widgets = {
#             "customer": forms.Select(attrs={"placeholder": "Prix", "class": "rounded-md w-32"}),
#             "product": forms.Select(attrs={"placeholder": "Produit", "class": "rounded-md w-32"}),
#             "quantity": forms.NumberInput(attrs={"placeholder": "Quantité", "class": "rounded-md w-32"}),
#             "price": forms.NumberInput(attrs={"placeholder": "Prix", "class": "rounded-md w-32"}),
#             "excecuted": forms.Select(attrs={"class": "rounded-md w-32"}),
#             "add_date": forms.DateInput(attrs={"class": "rounded-md w-32"}),
#         }
#         labels = {
#             "customer": "",
#             "product": "",
#             "quantity": "",
#             "price": "",
#             "add_date": "",
#             "excecuted": "",
#
#         }
