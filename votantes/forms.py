from django import forms
from usuarios.models import Usuario
from corporaciones.models import Corporacion
from votantes.models import Votante

"""
Este formulario se encuentran los datos para registrar el votante
"""
class FormularioRegistroVotante(forms.Form):

    cedula_usuario = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí la cedula de usuario', 'min':'1' , 'required':'true'}))

    nombre_usuario = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí el nombre del usuario', 'required':'true'}))

    apellido_usuario = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí el apellido  del usuario', 'required':'true'}))


    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí su correo electronico', 'required':'true'}))

    codigo_estudiante = forms.IntegerField(
       required=False,  widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí el códido de estudiante', 'min':'1' , 'required':'false'}))

    plan_estudiante = forms.ModelChoiceField(queryset=Corporacion.objects.filter(facultad__isnull=False), required=False, empty_label=None)


    def usuariovotante_existe(self):
        diccionario_limpio = self.cleaned_data
        cedula = diccionario_limpio.get('cedula_usuario')
        votante = Votante.usuario.objects.get(username=cedula)

        if not votante is None:
            raise self.ValidationError("El votante ya existe")
        return cedula

class FormularioEditarVotante(forms.Form):

    cedula_usuario = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí la cedula de usuario', 'min':'1' , 'required':'true'}))

    nombre_usuario = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí el nombre del usuario', 'required':'true'}))

    apellido_usuario = forms.CharField(
        widget=forms.TextInput( attrs={'class': 'form-control', 'placeholder': 'Escriba aquí el apellido  del usuario', 'required':'true'}))

    esta_activo = forms.BooleanField(initial=True, required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox form-icon'}))

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí su correo electronico', 'required':'true'}))

    codigo_estudiante = forms.IntegerField(
       required=False,  widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí el códido de estudiante', 'min':'1', 'required':'false'}))

    plan_estudiante = forms.ModelChoiceField(queryset=Corporacion.objects.filter(facultad__isnull=False), required=False, empty_label=None)


class FormularioCargar(forms.Form):
    file = forms.FileField(label='Seleccionar un archivo' , widget=forms.FileInput(attrs={'accept':".csv"}))
