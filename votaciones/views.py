from django.contrib.auth.decorators import permission_required
from planchas.models import Plancha
from usuarios.models import Usuario
from votantes.models import Votante
from django.db.models import Q
from jornadas.models import Jornada_Corporacion
from corporaciones.models import Corporacion
from datetime import datetime
from votaciones.models import Votacion_Log


from django.shortcuts import render_to_response, render, redirect
from django.utils import timezone
from django.conf import settings
timezone.activate(settings.TIME_ZONE)

def mostrar_tarjeton(request):
    # Votar

    id_jornada_corporacion = request.session.pop("id_jornada_corporacion", None)
    print("id_jornada_corporacion:" , id_jornada_corporacion)

    if request.POST:

        # Sumando el voto a la plancha
        value_plancha = request.POST['value_plancha']
        print("plancha a votar : " , value_plancha)
        plancha_a_sumar_voto = Plancha.objects.get(id=value_plancha)
        plancha_a_sumar_voto.num_votos += 1
        try:
            plancha_a_sumar_voto.save()
        except Exception as e:
            print(e)

        # Creando el LOG
        votante_log = Votacion_Log()
        votante_log.jornada_corporacion = plancha_a_sumar_voto.jornada_corporacion
        votante_log.usuario = Usuario.objects.get(cedula_usuario =request.user.username)

        try:
            votante_log.save()
        except Exception as e:
            print(e)



        return redirect('login')
    elif id_jornada_corporacion is not None:
        planchas = Plancha.objects.filter(is_active=True, jornada_corporacion_id=id_jornada_corporacion)

        try:
            plancha_voto_en_blanco = planchas.get(numeroplancha=0)
        except Exception as e:
            print("voto en blanco")
            return redirect("login")

        print(plancha_voto_en_blanco)
        jornada_corporacion = Jornada_Corporacion.objects.get(id=id_jornada_corporacion)
        return render(request, "mostrar_tarjeton.html", {"jornada_corporacion": jornada_corporacion, 'planchas':planchas , 'plancha_voto_en_blanco':plancha_voto_en_blanco})
    else:
        return redirect('login')


def mostrar_corporaciones(request, usuario, votantes_asociados, jornada):

    #print('votantes' , votantes_asociados.values_list('plan' , flat=True))
    #print('usuario' , usuario)
    #print('jornada' ,jornada)

    if request.POST and "btnCorporacion" in request.POST:
        id_jornada_corporacion = request.POST["btnCorporacion"]
        request.session['id_jornada_corporacion'] = id_jornada_corporacion
        return redirect('mostrar_tarjeton')
    else:
        #votantes_asociados = Votante.objects.filter(usuario__cedula_usuario=request.user.username)

        # Corporaciones activas de la jornada
        jornada_corporaciones_activas = Jornada_Corporacion.objects.filter(jornada_id=jornada.id, is_active=True)
        #print(jornada_corporaciones_activas)

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


        corporaciones_ya_votadas = Votacion_Log.objects.filter(is_active=True,
                                    usuario__cedula_usuario=request.user.username).values_list('jornada_corporacion__corporacion__id_corporation' , flat=True)

        #print(corporaciones_ya_votadas)

        return render(request, 'votacion.html', {'jornada_corporaciones_activas':jornada_corporaciones_activas ,
                                                 'corporaciones_ya_votadas':corporaciones_ya_votadas })

def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)
