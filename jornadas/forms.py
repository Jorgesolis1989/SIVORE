from django import forms
from corporaciones.models import Corporacion

"""
Este formulario se encuentran los datos para registrar una jornada
"""
class FormularioRegistroJornada(forms.Form):

    nombre_jornada = forms.CharField()

    fecha_jornada = forms.DateField()

    hora_inicio = forms.DateTimeInput()

    hora_final = forms.DateTimeInput()

    corporaciones = forms.ModelChoiceField(widget=forms.Select(attrs={'multiple tabindex':'4', 'data-placeholder':'Escoger las corporaciones'}), queryset=Corporacion.objects.all(), required=True, empty_label=None)


