from django import forms
from corporaciones.models import Corporacion

"""
Este formulario se encuentran los datos para registrar una jornada
"""
class FormularioRegistroJornada(forms.Form):

    nombre_jornada = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí el nombre de la jornada', 'required':'true', 'data-width':'100%'}))

    fecha_jornada = forms.DateField(input_formats='%d/%m/%y',widget=forms.DateInput(attrs={'type':'text', 'class':'form-control', 'required':'true'}))

    hora_inicio = forms.TimeField(input_formats='%H:%M %p', widget=forms.TimeInput(attrs={'id':'demo-tp-com', 'type':'text', 'class':'form-control', 'required':'true'}))

    hora_final = forms.TimeField(input_formats='%H:%M %p', widget=forms.TimeInput(attrs={'id':'demo-tp-com-1', 'type':'text', 'class':'form-control', 'required':'true'}))

    corporaciones = forms.ModelChoiceField(widget=forms.Select(attrs={'id':'demo-cs-multiselect', 'data-live-search':'true',
                                                                      'multiple tabindex':'4', 'data-placeholder':'Escoger las corporaciones'}),
                                           queryset=Corporacion.objects.all(), required=True, empty_label=None)


