from django.contrib.auth.decorators import permission_required
from planchas.models import Plancha
from votantes.models import Votante
from django.db.models import Q
from jornadas.models import Jornada_Corporacion
from corporaciones.models import Corporacion
from datetime import datetime
from django.shortcuts import render_to_response, render, redirect

def mostrar_tarjeton(request):
    return render(request, 'mostrar_tarjeton.html')

def mostrar_corporaciones(request, usuario, votantes, jornada):

    if request.POST and "btnCorporacion" in request.POST:
        id_jornada_corporacion = request.POST["btnCorporacion"]
        planchas = Plancha.objects.filter(is_active=True, jornada_corporacion_id=id_jornada_corporacion)
        jornada_corporacion = Jornada_Corporacion.objects.get(id=id_jornada_corporacion)
        return render(request, "mostrar_tarjeton.html", {"jornada_corporacion": jornada_corporacion, 'planchas':planchas})
    else:
        votantes_asociados = Votante.objects.filter(usuario__cedula_usuario=request.user.username)

        # Corporaciones activas de la jornada
        corporaciones_activas_jornada = Jornada_Corporacion.objects.filter(Q(jornada__fecha_inicio_jornada__lte = datetime.now()) ,
                                                                  jornada__is_active=True,
                                                                  jornada__fecha_final_jornada__gte = datetime.now())

        #print(corporaciones_activas_jornada)
        # Corporaciones que estan permitidas por el usuario
        corporaciones = []
        for votante in votantes_asociados:
                corporaciones += (Corporacion.objects.filter(Q(id_corporation=votante.plan.facultad.id_corporation) |
                                         Q(id_corporation=votante.plan.id_corporation)).values_list("id_corporation" , flat=True))

        corporaciones_activas_jornada = corporaciones_activas_jornada.filter(
                Q(corporacion__id_corporation=1) |
                Q(corporacion__id_corporation=2) |
                Q(corporacion__id_corporation__in=corporaciones)).order_by("corporacion__id_corporation")
        #print(corporaciones_activas_jornada)
        return render(request, 'votante.html', {'corporaciones_activas':corporaciones_activas_jornada})