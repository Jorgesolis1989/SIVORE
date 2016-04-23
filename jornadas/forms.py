from django import forms
from corporaciones.models import Corporacion
from jornadas.models import Jornada_Corporacion
from django.db.models import Q
"""
Este formulario se encuentran los datos para registrar una jornada
"""
class FormularioRegistroJornada(forms.Form):

    nombre_jornada = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí el nombre de la jornada', 'required':'true', 'data-width':'100%'}))

    fecha_jornada = forms.CharField( widget=forms.DateInput(attrs={'type':'text', 'class':'form-control', 'required':'true'}))

    hora_inicio = forms.CharField( widget=forms.TimeInput(attrs={'id':'demo-tp-com', 'type':'text', 'class':'form-control', 'required':'true'}))

    hora_final = forms.CharField( widget=forms.TimeInput(attrs={'id':'demo-tp-com-1', 'type':'text', 'class':'form-control', 'required':'true'}))

    corporaciones = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple(attrs={'id':'demo-cs-multiselect', 'data-live-search':'true',
                                                                      'multiple tabindex':'4', 'data-placeholder':'Escoger las corporaciones'}),
                                           queryset=Corporacion.objects.all().exclude(Q(id_corporation=0)  | Q(id_corporation__in=Jornada_Corporacion.objects.filter(jornada__is_active=True).values_list("corporacion__id_corporation" , flat=True))), required=True)


