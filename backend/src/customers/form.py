from django import forms

from customers.models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ("name",
                  "prenom",
                  "localisation",
                  "numero",)

        widgets = {
            "name": forms.TextInput(attrs={"placeholder":"Nom", "class": "rounded-md" ,"style":"width:300px;"}),
            "prenom": forms.TextInput(attrs={"placeholder":"Prénom", "class": "rounded-md" ,"style":"width:300px;"}),
            "localisation": forms.TextInput(attrs={"placeholder":"Localisation", "class": "rounded-md" ,"style":"width:300px;"}),
            "numero": forms.TextInput(attrs={"placeholder":"Numero", "class": "rounded-md" ,"style":"width:300px;"})
        }
        labels = {
            "name":"",
            "prenom":"",
            "localisation":"",
            "numero":"",
        }