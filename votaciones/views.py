from django.contrib.auth.decorators import permission_required
from planchas.models import Plancha
from votantes.models import Votante
from django.db.models import Q
from jornadas.models import Jornada_Corporacion
from corporaciones.models import Corporacion
from datetime import datetime

from django.shortcuts import render_to_response, render, redirect
from django.utils import timezone
from django.conf import settings
timezone.activate(settings.TIME_ZONE)

def mostrar_tarjeton(request):
    # Votar

    id_jornada_corporacion = request.session.pop("id_jornada_corporacion", None)
    if request.POST:
        print("Voté")
        return redirect('login')
    elif id_jornada_corporacion is not None:
        planchas = Plancha.objects.filter(is_active=True, jornada_corporacion_id=id_jornada_corporacion)
        jornada_corporacion = Jornada_Corporacion.objects.get(id=id_jornada_corporacion)
        return render(request, "mostrar_tarjeton.html", {"jornada_corporacion": jornada_corporacion, 'planchas':planchas})
    else:
        return redirect('login')


def mostrar_corporaciones(request, usuario, votantes_asociados, jornada):

    print('votantes' , votantes_asociados.values_list('plan' , flat=True))
    print('usuario' , usuario)
    print('jornada' ,jornada)

    if request.POST and "btnCorporacion" in request.POST:
        id_jornada_corporacion = request.POST["btnCorporacion"]
        request.session['id_jornada_corporacion'] = id_jornada_corporacion
        return redirect('mostrar_tarjeton')
    else:
        #votantes_asociados = Votante.objects.filter(usuario__cedula_usuario=request.user.username)

        # Corporaciones activas de la jornada
        jornada_corporaciones_activas = Jornada_Corporacion.objects.filter(jornada_id=jornada.id, is_active=True)
        print(jornada_corporaciones_activas)

        #print(corporaciones_activas_jornada)
        #Jornada Corporaciones que estan permitidas por el usuario
        corporaciones = []
        for votante in votantes_asociados:
                corporaciones += (Corporacion.objects.filter(Q(id_corporation=votante.plan.facultad.id_corporation) |
                                         Q(id_corporation=votante.plan.id_corporation)).values_list("id_corporation" , flat=True))


        jornada_corporaciones_activas = jornada_corporaciones_activas.filter(
                # La de consejo superior
                Q(corporacion__id_corporation=1) |
                # Consejo académico
                Q(corporacion__id_corporation=2) |
                # las que el puede
                Q(corporacion__id_corporation__in=corporaciones)).order_by("corporacion__id_corporation")


        return render(request, 'votacion.html', {'jornada_corporaciones_activas':jornada_corporaciones_activas})

def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)
