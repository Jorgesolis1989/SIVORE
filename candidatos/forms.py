from django import forms
from candidatos.models import Candidato
from corporaciones.models import Corporacion
from votantes.models import Votante
from jornadas.models import Jornada_Corporacion
from django.db.models import Q
"""
Este formulario se encuentran los datos para registrar un candidato
"""
class FormularioRegistroCandidato(forms.Form):

    """
    *******************************************  Consultas para el campo votantes **********************
    """
    ### Consulta corporaciones que se eligiran
    corporaciones_que_se_eligiran = Corporacion.objects.filter(id_corporation__in= (Jornada_Corporacion.objects.filter(jornada__is_active=True).values_list("corporacion__id_corporation", flat=True)))

    # votantes que pueden votar ser elegidos en las corporaciones que estan permitidas
    votantes_que_pueden_ser_candidatos = Votante.objects.filter((Q(plan__in= corporaciones_que_se_eligiran) | Q(plan__facultad__in=corporaciones_que_se_eligiran)) , is_active=True)

    # excluimos los votantes que ya estan como candidatos
    votantes_que_pueden_ser_candidatos = votantes_que_pueden_ser_candidatos.exclude(codigo__in=Candidato.objects.filter(is_active=True).values_list('votante__codigo', flat=True))

    """
    **********************************************************************************
    """

    # Modulo votantes.
    votante = forms.ModelChoiceField(widget=forms.Select(attrs={'onchange':'this.form.submit()','class':'selectpicker', 'data-live-search':'true',
                                                                 'data-width':'100%'}), queryset=votantes_que_pueden_ser_candidatos, required=True, empty_label=None)

    foto = forms.ImageField(label="Escoja la foto del candidato", required=False, widget=forms.FileInput(attrs={'class':'form-control', 'accept':".jpg, .png, .jpeg, .gif, .bmp, .tif, .tiff|images/*"}))

    CHOICES = [('Principal','Principal'), ('Suplente','Suplente')]
    tipo_candidato = forms.ChoiceField(widget=forms.Select(attrs={'class': 'selectpicker', 'data-width':'100%'}),required=True, choices=CHOICES )

    """
    *******************************************  Consultas para el campo corporaciones **********************
    """
    corporaciones_habilitadas = Jornada_Corporacion.objects.filter(jornada__is_active=True)

    corporacion_candidato = corporaciones_habilitadas.filter(Q(corporacion__id_corporation=votantes_que_pueden_ser_candidatos[0].plan.id_corporation) |
                                                             Q(corporacion__id_corporation=votantes_que_pueden_ser_candidatos[0].plan.facultad.id_corporation))


    corporacion = forms.ModelChoiceField( widget=forms.Select(attrs={'class':'selectpicker', 'data-live-search':'true'
                                                                ,'data-width':'100%'}), queryset=corporacion_candidato, required=True, empty_label=None)

    def candidato_nulo(self):
        diccionario_limpio = self.cleaned_data
        votante = diccionario_limpio.get('votante')
        if votante is None:
            print("validador")
            raise self.ValidationError("El votante no puede ser nulo")

    def candidato_existe(self):
        diccionario_limpio = self.cleaned_data
        cedula = diccionario_limpio.get('cedula_candidato')
        candidato = Candidato.objects.get(cedula_candidato=cedula)

        if not candidato is None:
            raise self.ValidationError("El candidato ya existe")
        return cedula

"""
Este formulario se encuentran los datos para editar un candidato
"""
class FormularioEditarCandidato(forms.Form):

    votante = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control', 'data-live-search':'true',
                                                                 'data-width':'100%', 'disabled': 'False'}), required=False)
    nombrefoto = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'disabled': 'False'}), required=False)

    foto = forms.ImageField(label="Escoja la foto del candidato", required=False, widget=forms.FileInput(attrs={'class':'form-control', 'accept':".jpg, .png, .jpeg, .gif, .bmp, .tif, .tiff|images/*"}))

    CHOICES = [('Principal','Principal'), ('Suplente','Suplente')]

    tipo_candidato = forms.ChoiceField(widget=forms.Select(attrs={'class': 'selectpicker', 'data-width':'100%'}),required=True, choices=CHOICES )

    corporacion = forms.ModelChoiceField(widget=forms.Select(attrs={'class':'selectpicker'
                                                              ,'data-width':'100%'}), queryset=Jornada_Corporacion.objects.all(), required=True, empty_label=None)

