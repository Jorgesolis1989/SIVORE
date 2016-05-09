from django import forms
from candidatos.models import Candidato
from jornadas.models import Jornada_Corporacion
from planchas.models import Plancha
from django.db.models import Q

"""
Este formulario se encuentran los datos para registrar una plancha
"""
class FormularioRegistroPlancha(forms.Form):

    numeroplancha = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí el número de la plancha', 'min':'1', 'required':'true'}))

    jornada_corporaciones = Jornada_Corporacion.objects.filter(jornada__is_active=True).order_by("jornada__fecha_inicio_jornada")

    jornada_corporacion = forms.ModelChoiceField(widget=forms.Select(attrs={'onchange':'this.form.submit()','class':'selectpicker', 'data-live-search':'true',
                                                                 'data-width':'100%'}), queryset=jornada_corporaciones, required=True, empty_label=None)

    candidato_principal = forms.ModelChoiceField(widget=forms.Select(attrs={'class':'selectpicker', 'data-live-search':'true',
                                                                            'data-width':'100%'}), queryset=Candidato.objects.all(), required=True, empty_label=None)

    candidato_suplente = forms.ModelChoiceField(widget=forms.Select(attrs={'class':'selectpicker', 'data-live-search':'true',
                                                                            'data-width':'100%'}), queryset=Candidato.objects.all(), required=False)

    url_propuesta = forms.URLField(required=False , widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese aquí el enlace web de la propuesta de trabajo'}))

    def plancha_nulo(self):
        diccionario_limpio = self.cleaned_data
        candidato = diccionario_limpio.get('candidato')
        if candidato is None:
            raise self.ValidationError("El candidato no puede ser nulo")

    def plancha_existe(self):
        diccionario_limpio = self.cleaned_data
        numeroplancha = diccionario_limpio.get('numeroplancha')
        plancha = Plancha.objects.get(numeroplancha=numeroplancha)

        if not plancha is None:
            raise self.ValidationError("La plancha ya existe")
        return numeroplancha

"""
Este formulario se encuentran los datos para editar una plancha
"""
class FormularioEditarPlancha(forms.Form):

    numeroplancha = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min':'1', 'required':'true'}))

    corporacion = forms.ModelChoiceField(widget=forms.Select(attrs={'disabled':'false','onchange':'this.form.submit()','class':'selectpicker', 'data-live-search':'true',
                                                                 'data-width':'100%'}), queryset=Jornada_Corporacion.objects.filter(jornada__is_active=True), required=False)

    #las dos siguientes instrucciones son consultas de los candidatos (principal, suplente) asociados a una corporacion determinada
    consulta_candidato_principal = Candidato.objects.filter(tipo_candidato__exact='Principal')
    consulta_candidato_suplente = Candidato.objects.filter(tipo_candidato__exact='Suplente')

    candidato_principal = forms.ModelChoiceField(widget=forms.Select(attrs={'class':'selectpicker', 'data-live-search':'true',
                                                                            'data-width':'100%'}), queryset=consulta_candidato_principal, required=True, empty_label=None)

    candidato_suplente = forms.ModelChoiceField(widget=forms.Select(attrs={'class':'selectpicker', 'data-live-search':'true',
                                                                            'data-width':'100%'}), queryset=consulta_candidato_suplente, required=False)

    url_propuesta = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-control'}))
