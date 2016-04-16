from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response, render, redirect
from jornadas.forms import FormularioRegistroJornada

@permission_required("usuarios.Administrador", login_url="/")

def registro_jornada(request):
    #Verificación para crear una jornada
    form = FormularioRegistroJornada()

    return render(request, 'registro_jornada.html', {'form': form})

