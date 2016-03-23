from django import forms
from usuarios.models import Usuario
"""Este formulario se encuentran los datos para logueo del usuario
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
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí la cedula de usuario', 'min':'1' }))

    nombre_usuario = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí el nombre del usuario'}))

    apellido_usuario = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí el apellido  del usuario'}))

    CHOICES = [('Administrador','Administrador'), ('Votante','Votante'), ('Superior','Superior') ]
    rol = forms.ChoiceField(widget=forms.RadioSelect()   , choices=CHOICES)

    esta_activo = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox form-icon'}))

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí su correo electronico'}))

    def usuario_existe(self):
        diccionario_limpio = self.cleaned_data
        cedula = diccionario_limpio.get('cedula_usuario')
        usuario = Usuario.objects.get(username=cedula)

        if not usuario is None:
            raise self.ValidationError("El usuario ya existe")
        return cedula

class FormularioEditarUsuario(forms.Form):

    cedula_usuario = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí la cedula de usuario', 'min':'1'}))

    nombre_usuario = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí el nombre del usuario'}))

    apellido_usuario = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí el apellido  del usuario'}))

    CHOICES = [('Administrador','Administrador'), ('Votante','Votante'), ('Superior','Superior') ]
    rol = forms.ChoiceField(widget=forms.RadioSelect()   , choices=CHOICES)

    esta_activo = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox form-icon'}))

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí su correo electronico'}))


class FormularioCargar(forms.Form):
    file = forms.FileField(label='Seleccionar un archivo')


