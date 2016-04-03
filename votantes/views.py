from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response, redirect, render
from votantes.models import Votante


# Vista para listar votantes
@permission_required("usuarios.Administrador", login_url="/")
def listar_votantes(request):
    votantes = Votante.objects.all()
    llamarMensaje = request.session.pop('llamarMensaje', None)
    mensaje = request.session.pop('mensaje', None)
    varvotante ="votante"

    return render(request, 'listar_votantes.html', {'votantes': votantes,'llamarMensaje': llamarMensaje,'mensaje': mensaje, 'varvotante' : varvotante})

