from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response, render, redirect
from jornadas.forms import FormularioRegistroJornada
from jornadas.models import Jornada , Jornada_Corporacion



@permission_required("usuarios.Administrador", login_url="/")
def registro_jornada(request):
    #Verificación para crear una jornada
    form = FormularioRegistroJornada()
    return render(request, 'registro_jornada.html', {'form': form})

# Vista para listar votantes
@permission_required("usuarios.Administrador", login_url="/")
def listar_jornadas(request):
    corporaciones_jornada = Jornada_Corporacion.objects.filter(jornada__is_active=True)
    llamarMensaje = request.session.pop('llamarMensaje', None)
    mensaje = request.session.pop('mensaje', None)
    return render(request,  'listar_jornadas.html', {'corporaciones_jornada': corporaciones_jornada, 'llamarMensaje': llamarMensaje,'mensaje': mensaje})

