from django import forms

from .models import Supplier, SupplierInvoices, SupplierInvoiceItems


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = (
            'name',
            'address',
            'phone',
            'email'
        )
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Dénomination", "class": "rounded-md w-56"}),
            "address": forms.TextInput(attrs={"placeholder": "Adresse", "class": "rounded-md w-56"}),
            "phone": forms.TextInput(attrs={"placeholder": "Téléphone", "class": "rounded-md w-56"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email", "class": "rounded-md w-56"}),

        }

        labels = {
            "name": "",
            "address": "",
            'phone': "",
            'email': "",
        }


# class NewStockForm(forms.ModelForm):
#     class Meta:
#         model = NewStock
#         fields = [
#             "invoice",
#             "product",
#             "quantity",
#             "price",
#             "add_date",
#         ]
#         widgets = {
#             "invoice": forms.Select(attrs={"placeholder": "Produit", "class": "rounded-md", "style": "width:210px;"}),
#             "product": forms.Select(attrs={"placeholder": "Produit", "class": "rounded-md", "style": "width:210px;"}),
#             "quantity": forms.NumberInput(attrs={"placeholder": "Quantité", "class": "rounded-md w-60"}),
#             "price": forms.NumberInput(attrs={"placeholder": "Prix Fournisseur", "class": "rounded-md w-60"}),
#             "add_date": forms.DateInput(attrs={"class": "rounded-md w-60"}),
#
#         }
#         labels = {
#             "invoice": "",
#             "product": "",
#             "quantity": "",
#             "price": "",
#             "add_date": "",
#         }
#
#     # class Meta:
#     #     model = Supplier
#     #     fields = ['name', 'address', 'phone', 'email']
#     #
#     # widgets = {
#     #     "name": forms.TextInput(attrs={"placeholder": "Qunatité", "class": "rounded-md w-36"}),
#     #     "address": forms.TextInput(attrs={"placeholder": "Qunatité", "class": "rounded-md w-36"}),
#     #     "phone": forms.TextInput(attrs={"placeholder": "Qunatité", "class": "rounded-md w-36"}),
#     #     # "email": forms.EmailInput(attrs={"placeholder": "Qunatité", "class": "rounded-md w-36"}),
#     # }
#     # labels = {
#     #     "name": "",
#     #     "address": "",
#     #     "phone": "",
#     #     "email": ""
#     # }

class SupplierInvoiceItemsForm(forms.ModelForm):
    class Meta:
        model = SupplierInvoiceItems
        fields = ["invoice",
                  "product",
                  "quantity",
                  "price",
                  "add_date"]
        widgets = {
            "invoice": forms.Select(attrs={"class": "rounded-md", "sytle": "width:100px;", "style": "display:none;"}, ),
            "product": forms.Select(attrs={"class": "rounded-md", "sytle": "width:200px;"}, ),
            "quantity": forms.NumberInput(attrs={"placeholder": "Qunatité", "class": "rounded-md w-36"}),
            "price": forms.NumberInput(attrs={"placeholder": "Prix", "class": "rounded-md w-36"}),
            "add_date": forms.NumberInput(attrs={"placeholder": "Prix", "class": "rounded-md w-36"})
        }
        labels = {
            "invoice": "",
            "product": "",
            "quantity": "",
            "price": "",
            "add_date":""
        }


class SupplierInvoicesForm(forms.ModelForm):
    class Meta:
        model = SupplierInvoices
        fields = ("supplier",)

# class SupplierInvoiceItemForm(forms.ModelForm):
#     class Meta:
#         model = SupplierInvoiceItem
#         fields = ["invoice",
#                     "product", "quantity", "price"] widgets = { "invoice": forms.Select(attrs={"class": "rounded-md",
#                     "sytle": "width:100px;", "style": "display:none;"}, ), "product": forms.Select(attrs={"class": "rounded-md",
#                     "sytle": "width:200px;"}, ), "quantity": forms.NumberInput(attrs={"placeholder": "Qunatité", "class": "rounded-md w-36"}), "price": forms.NumberInput(attrs={"placeholder": "Prix", "class": "rounded-md w-36"}) } labels = {
#                     "invoice": "", "product": "", "quantity": "", "price": "" }
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#


