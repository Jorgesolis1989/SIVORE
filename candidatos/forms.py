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

    corporaciones_habilitadas = Jornada_Corporacion.objects.filter(jornada__is_active=True)

    # id corporaciones que se van a elegir.
    corporaciones_que_se_eligiran = corporaciones_habilitadas.values_list("corporacion__id", flat=True)

    # votantes que pueden votar ser elegidos en las corporaciones que estan permitidas

    #Aqui revisamos si las corporaciones consejo superior o consejo académico se van a elegir
    if 1 or 2  in corporaciones_habilitadas.values_list("corporacion__id_corporation", flat=True):
        votantes_que_pueden_ser_candidatos = Votante.objects.filter(is_active=True)
    else:
    # Filtramos a los votantes según los programas académicos que se van a elegir.
        votantes_que_pueden_ser_candidatos = Votante.objects.filter(
            (Q(plan__id__in= corporaciones_que_se_eligiran) | Q(plan__facultad__id__in=corporaciones_que_se_eligiran)) & Q(is_active=True))

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

    if votantes_que_pueden_ser_candidatos:
        corporacion_candidato = corporaciones_habilitadas.filter(Q(corporacion__id=votantes_que_pueden_ser_candidatos[0].plan.id) |
                                                                Q(corporacion__id=votantes_que_pueden_ser_candidatos[0].plan.facultad.id) |
                                                                Q(corporacion__id_corporation=1) |
                                                                Q(corporacion__id_corporation=2))
    else:
        corporacion_candidato = corporaciones_habilitadas

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

