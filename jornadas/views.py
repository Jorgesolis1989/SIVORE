from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response, render, redirect
from jornadas.forms import FormularioRegistroJornada, FormularioEditarJornada
from planchas.models import Plancha
from candidatos.models import Candidato
from votantes.models import Votante
from usuarios.models import Usuario
from corporaciones.models import Corporacion
from datetime import datetime
from django.utils import timezone
from time import strptime
from django.utils.timezone import activate
from django.conf import settings
activate(settings.TIME_ZONE)
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
   jornadas = Jornada.objects.filter(is_active=True)
   llamarMensaje = request.session.pop('llamarMensaje', None)
   mensaje = request.session.pop('mensaje', None)
   return render(request,  'listar_jornadas.html', {'jornadas': jornadas, 'llamarMensaje': llamarMensaje,'mensaje': mensaje})

# funcion que permite la edición de la jornada seleccionada
@permission_required("usuarios.Administrador", login_url="/")
def editar_jornada(request, id):
    try:
        jornada = Jornada.objects.get(id = id)
    except jornada.DoesNotExist:
        llamarmensaje = "fracaso_usuario"
        mensaje = "La jornada #" + str(id)+ " no existe en el sistema."
        request.session["llamarmensaje"] = llamarmensaje
        request.session["mensaje"] = mensaje
        return redirect("listar_jornadas.html")

    if request.method == 'POST' and "btncreate" in request.POST:
        form = FormularioEditarJornada(request.POST)
        #Si el formulario es valido

        if form.is_valid():
            jornada.nombrejornada =  form.cleaned_data["nombre_jornada"]

            hora_completa = form.cleaned_data["fecha_jornada"] + " " + form.cleaned_data["hora_inicio"]
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

            mensaje = "Se editó la jornada " + jornada.nombrejornada + " exitosamente "
            llamarMensaje = "exito_usuario"
            request.session["mensaje"] = mensaje
            request.session["llamarMensaje"] = llamarMensaje
            return redirect(listar_jornadas)

        #si no es valido el formulario, crear
        else:
            mensaje = "Datos incompleto para editar la jornada"
            llamarMensaje = "fracaso_usuario"
            form = FormularioRegistroJornada()
            data = {'mensaje': mensaje, 'form': form, 'llamarMensaje':llamarMensaje}
            return render(request, 'editar_jornada.html', data)
    else:
        form = FormularioEditarJornada()

        # corporaciones de la jornada
        corporaciones_de_jornada = Corporacion.objects.filter(id_corporation__in=Jornada_Corporacion.objects.filter(jornada__id = jornada.id, jornada__is_active=True).values_list("corporacion__id_corporation" , flat=True))

        # lista de ids Corporaciones ocupadas
        corporaciones_ocupadas = Corporacion.objects.filter(id_corporation__in=Jornada_Corporacion.objects.filter(jornada__is_active=True).values_list("corporacion__id_corporation", flat=True))

        # Corporaciones libres
        corporaciones_libres= Corporacion.objects.all().exclude(id_corporation__in=corporaciones_ocupadas.exclude(id_corporation__in=corporaciones_de_jornada.values_list("id_corporation", flat=True)).values_list("id_corporation", flat=True))

        # Agregando las corporaciones de la jornada porque aparecen ocupadas
        form.fields["corporaciones"].queryset = corporaciones_libres

        #envio de datos al formulario editar
        form.initial = {'nombre_jornada' : jornada.nombrejornada, "fecha_jornada" : jornada.fecha_inicio_jornada.date().strftime("%m/%d/%Y"),
                        "hora_inicio" : timezone.localtime(jornada.fecha_inicio_jornada).strftime('%H:%M:%S'), "hora_final" : timezone.localtime(jornada.fecha_final_jornada).strftime('%H:%M:%S'), "corporaciones": [o for o in corporaciones_de_jornada]}
    return render(request, 'editar_jornada.html', {'form': form})
