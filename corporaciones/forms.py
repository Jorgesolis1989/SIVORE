from django import forms
from django.db.models import Q
from corporaciones.models import Corporacion

class FormularioRegistroCorporacion(forms.Form):

    id_corporation = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí el id de la corporación', 'min':'1' , 'required':'true'}))

    name_corporation = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí el nombre de la corporación', 'required':'true'}))

    facultad = forms.ModelChoiceField(queryset=Corporacion.objects.filter(is_active=True, facultad=None).exclude
    (Q(id_corporation=1) | Q(id_corporation=2) ), required=False, initial=None)

    def corporacion_existe(self):
        diccionario_limpio = self.cleaned_data
        id_corporation = diccionario_limpio.get('id_corporation')
        corporacion = Corporacion.objects.get(id_corporation=id_corporation)

        if not corporacion is None:
            raise self.ValidationError("La corporacion ya existe")
        return id_corporation

class FormularioEditarCorporacion(forms.Form):
    id_corporation = forms.IntegerField(
            widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí el id de la corporación', 'min':'1' , 'required':'true'}))

    name_corporation = forms.CharField(
            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí el nombre de la corporación', 'required':'true'}))

    facultad = forms.ModelChoiceField(queryset=Corporacion.objects.filter(name_corporation__contains="Facultad"), required=False)
