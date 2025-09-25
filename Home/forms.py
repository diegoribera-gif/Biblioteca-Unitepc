from django import forms
from .models import Libro


class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ["titulo", "autor", "editorial", "cantidad", "categoria"]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "autor": forms.TextInput(attrs={"class": "form-control"}),
            "editorial": forms.TextInput(attrs={"class": "form-control"}),
            "cantidad": forms.NumberInput(attrs={"class": "form-control"}),
            "categoria": forms.TextInput(attrs={"class": "form-control"}),
        }


