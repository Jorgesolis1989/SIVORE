from django import forms
from candidatos.models import Candidato
from corporaciones.models import Corporacion

"""
Este formulario se encuentran los datos para registrar un candidato
"""
class FormularioRegistroCandidato(forms.Form):

    cedula_candidato = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Seleccione el candidato', 'min':'1', 'required':'true'}))

    #foto = forms.ImageField(upload_to='folder/',  null=True, blank=True)

    CHOICES = [('Principal','Principal'), ('Suplente','Suplente')]
    tipo_candidato = forms.ChoiceField(widget=forms.Select(), required=True, choices=CHOICES)

    id_corporacion = forms.ModelChoiceField(queryset=Corporacion.objects.filter(name_corporation__contains="Facultad"), required=False, initial=None)


    def candidato_existe(self):
        diccionario_limpio = self.cleaned_data
        cedula = diccionario_limpio.get('cedula_candidato')
        candidato = Candidato.objects.get(cedula_candidato=cedula)

        if not candidato is None:
            raise self.ValidationError("El candidato ya existe")
        return cedula


