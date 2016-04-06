from django import forms
from candidatos.models import Candidato
from corporaciones.models import Corporacion
from votantes.models import Votante

"""
Este formulario se encuentran los datos para registrar un candidato
"""
class FormularioRegistroCandidato(forms.Form):

    votante = forms.ModelChoiceField( widget=forms.Select(attrs={'onchange':'this.form.submit()','class':'selectpicker', 'data-live-search':'true',
                                                                 'data-width':'100%'}),
                                      queryset=Votante.objects.exclude(codigo__in=Candidato.objects.all().values_list('votante__codigo', flat=True)), required=True, empty_label=None)
    foto = forms.ImageField(label="Escoja la foto del candidato", required=False, widget=forms.FileInput(attrs={'class':'form-control', 'accept':".jpg, .png, .jpeg, .gif, .bmp, .tif, .tiff|images/*"}))

    CHOICES = [('Principal','Principal'), ('Suplente','Suplente')]
    tipo_candidato = forms.ChoiceField(widget=forms.Select(attrs={'class': 'selectpicker', 'data-width':'100%'}),required=True, choices=CHOICES )

    corporacion = forms.ModelChoiceField( widget=forms.Select(attrs={'class':'selectpicker', 'data-live-search':'true'
                                                                 ,'data-width':'100%'}), queryset=Corporacion.objects.all(), required=True, empty_label=None)

    def candidato_existe(self):
        diccionario_limpio = self.cleaned_data
        cedula = diccionario_limpio.get('cedula_candidato')
        candidato = Candidato.objects.get(cedula_candidato=cedula)

        if not candidato is None:
            raise self.ValidationError("El candidato ya existe")
        return cedula


