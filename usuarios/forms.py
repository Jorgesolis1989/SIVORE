from django import forms
from usuarios.models import Usuario
from corporaciones.models import  Corporacion
from django.contrib.auth.models import User
from django.forms import ModelForm

"""
Este formulario se encuentran los datos para logueo del usuario
"""
class FormularioLogin(forms.Form):
    username = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí su cedula'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí su contraseña'}))

    def validar_cedula(self):
        diccionario_limpio = self.cleaned_data
        cedula = diccionario_limpio.get('username')
        if cedula != int:
            raise forms.ValidationError("La cedula debe de ser enteros")
        return cedula

"""
Este formulario se encuentran los datos para registrar el  usuario
"""
class FormularioRegistroUsuario(forms.Form):

    cedula_usuario = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí la cedula de usuario', 'min':'1' , 'required':'true'}))

    nombre_usuario = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí el nombre del usuario', 'required':'true'}))

    apellido_usuario = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí el apellido  del usuario', 'required':'true'}))

    CHOICES = [('Administrador','Administrador'), ('Votante','Votante'), ('Superior','Superior') ]
    rol = forms.ChoiceField(widget=forms.RadioSelect(attrs={'onClick': "showfieldvotantes('FormularioRegistroUsuario')"}), choices=CHOICES)

    esta_activo = forms.BooleanField( initial=True, required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox form-icon'}))

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí su correo electronico', 'required':'true'}))

    codigo_estudiante = forms.IntegerField(
       required=False,  widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí el códido de estudiante', 'min':'1' , 'required':'false'}))

    plan_estudiante = forms.ModelChoiceField(queryset=Corporacion.objects.filter(facultad__isnull=False), required=False, empty_label=None)


    def usuario_existe(self):
        diccionario_limpio = self.cleaned_data
        cedula = diccionario_limpio.get('cedula_usuario')
        usuario = Usuario.objects.get(username=cedula)

        if not usuario is None:
            raise self.ValidationError("El usuario ya existe")
        return cedula

class FormularioEditarUsuario(forms.Form):

    cedula_usuario = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí la cedula de usuario', 'min':'1' , 'required':'true'}))

    nombre_usuario = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí el nombre del usuario', 'required':'true'}))

    apellido_usuario = forms.CharField(
        widget=forms.TextInput( attrs={'class': 'form-control', 'placeholder': 'Escriba aquí el apellido  del usuario', 'required':'true'}))

    CHOICES = [('Administrador','Administrador'), ('Votante','Votante'), ('Superior','Superior') ]
    rol = forms.ChoiceField(widget=forms.RadioSelect(attrs={'onClick': "showfieldvotantes('FormularioEditarUsuario')"}), choices=CHOICES)


    esta_activo = forms.BooleanField(initial=True, required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox form-icon'}))

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí su correo electronico', 'required':'true'}))

    codigo_estudiante = forms.IntegerField(
       required=False,  widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí el códido de estudiante', 'min':'1' , 'required':'false'}))

    plan_estudiante = forms.ModelChoiceField(queryset=Corporacion.objects.filter(facultad__isnull=False), required=False, empty_label=None)


class FormularioCargar(forms.Form):
    file = forms.FileField(label='Seleccionar un archivo')
