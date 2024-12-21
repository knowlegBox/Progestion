from django import forms

from transactions.models import Versement, DailySpend


# class FactureForm(forms.ModelForm):
#     class Meta:
#         model = Facture
#         fields = ("user",
#                   "value",
#                   # "product",
#                   )
#         widgets = {
#             "user": forms.Select(attrs={"placeholder": "Client", "style": "width:215px;"}),
#             "value": forms.NumberInput(attrs={"placeholder": "Montant", "class": "rounded-md w-62"}),
#             # "product": forms
#         }
#         labels = {
#             "user": "",
#             "value": "",
#             # "product": ""
#         }


class VersementForm(forms.ModelForm):
    class Meta:
        model = Versement
        fields = ("user",
                  "supplier",
                  "recipient_type",
                  "amount",)
        widgets = {
            "user": forms.Select(attrs={"placeholder": "client", "class": "rounded-md", "style": "width:215px;"}),
            "supplier": forms.Select(attrs={"placeholder": "client", "class": "rounded-md", "style": "width:215px;"}),
            "recipient_type":forms.Select(attrs={"placeholder": "client", "class": "rounded-md", "style": "width:215px;"}),
            "amount": forms.NumberInput(attrs={"placeholder": "Montant", "class": "rounded-md w-62"})
        }
        labels = {
            "user": "",
            "supplier": "",
            "recipient_type": "",
            "amount": ""
        }


class SpendForm(forms.ModelForm):
    class Meta:
        model = DailySpend
        fields = (
            "name",
            "value",
            "add_date",
            "observation",
        )
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Désignation", "class": "rounded-md w-58"}),
            "value": forms.NumberInput(attrs={"placeholder": "Montant", "class": "rounded-md w-58"}),
            "observation": forms.Textarea(
                attrs={"placeholder": "Observation", "cols": "25", "rows": "3", "class": "rounded-md w-58"}),
            "add_date": forms.DateInput(attrs={"placeholder": "Date", "class": "rounded-md w-58"}),
        }
        labels = {
            "name": "",
            "value": "",
            "add_date": "",
            "observation": "",
        }
