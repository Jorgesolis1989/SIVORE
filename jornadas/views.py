from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response, render, redirect
from jornadas.forms import FormularioRegistroJornada
from planchas.models import Plancha
from candidatos.models import Candidato
from votantes.models import Votante
from usuarios.models import Usuario
from corporaciones.models import Corporacion
from datetime import datetime
from django.utils import timezone
from time import strptime

from jornadas.models import Jornada , Jornada_Corporacion


def ingresar_plancha_voto_blanco(jornada_corporacion):

    # Creando la plancha con el candidato voto en blanco para esa corporacion especifica
    plancha_voto_en_blanco = Plancha()
    plancha_voto_en_blanco.candidato_principal = None
    plancha_voto_en_blanco.is_active = True
    plancha_voto_en_blanco.jornada_corporacion = jornada_corporacion
    plancha_voto_en_blanco.numeroplancha = 0
    try:
        plancha_voto_en_blanco.save()
    except Exception as e:
        print(e)



@permission_required("usuarios.Administrador", login_url="/")
def registro_jornada(request):
    #Verificación para crear una jornada
    if request.method == 'POST' and  "btncreate" in request.POST:
        form = FormularioRegistroJornada(request.POST)
        #Si el formulario es valido

        if form.is_valid():
            jornada = Jornada()
            jornada.nombrejornada =  form.cleaned_data["nombre_jornada"]

            hora_completa = form.cleaned_data["fecha_jornada"] +   " "+  form.cleaned_data["hora_inicio"]
            jornada.fecha_inicio_jornada = datetime.strptime(hora_completa, "%m/%d/%Y %I:%M %p")
            jornada.fecha_inicio_jornada = timezone.make_aware(jornada.fecha_inicio_jornada,
                                                               timezone.get_current_timezone())

            hora_completa = form.cleaned_data["fecha_jornada"] +   " "+  form.cleaned_data["hora_final"]
            jornada.fecha_final_jornada = datetime.strptime(hora_completa, "%m/%d/%Y %I:%M %p")
            jornada.fecha_final_jornada = timezone.make_aware(jornada.fecha_final_jornada,
                                                               timezone.get_current_timezone())

            try:
                jornada.save()
            except Exception as e:
                print(e)
            # Creando la jornada electoral y habilitando las corporaciones.
            corporaciones = form.cleaned_data["corporaciones"]
            print(corporaciones)

            for corporacion in corporaciones:
                jornada_corporacion = Jornada_Corporacion()
                #guardamos jornada
                jornada_corporacion.jornada = jornada
                #guardamos corporacion
                jornada_corporacion.corporacion = corporacion
                try:
                    jornada_corporacion.save()
                except Exception as e:
                    print(e)

                # Ingresando candidato voto en blanco a la corporacion a elegir
                ingresar_plancha_voto_blanco(jornada_corporacion)


            mensaje = "Se creó la jornada "+jornada.nombrejornada+" exitosamente "
            llamarMensaje = "exito_usuario"
            request.session["mensaje"] = mensaje
            request.session["llamarMensaje"] = llamarMensaje
            return redirect(listar_jornadas)

        #si no es valido el formulario, crear
        else:
            mensaje = "Datos incompleto para crear la jornada"
            llamarMensaje = "fracaso_usuario"
            form = FormularioRegistroJornada()
            data = {'mensaje': mensaje, 'form': form, 'llamarMensaje':llamarMensaje}
            return render(request, 'registro_jornada.html', data)

    else:
        form = FormularioRegistroJornada()
        return render(request, 'registro_jornada.html', {'form': form})

# Vista para listar votantes
@permission_required("usuarios.Administrador", login_url="/")
def listar_jornadas(request):
    corporaciones_jornada = Jornada_Corporacion.objects.filter(jornada__is_active=True)
    llamarMensaje = request.session.pop('llamarMensaje', None)
    mensaje = request.session.pop('mensaje', None)
    return render(request,  'listar_jornadas.html', {'corporaciones_jornada': corporaciones_jornada, 'llamarMensaje': llamarMensaje,'mensaje': mensaje})



