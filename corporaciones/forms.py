from django import forms
from corporaciones.models import Corporacion

class FormularioRegistroCorporacion(forms.Form):

    id_corporation = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí el id de la corporación', 'min':'1' , 'required':'true'}))

    name_corporation = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí el nombre de la corporación', 'required':'true'}))

    facultad = forms.ModelChoiceField(queryset=Corporacion.objects.all(), required=False)

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

    facultad = forms.ModelChoiceField(queryset=Corporacion.objects.all(), required=False)
