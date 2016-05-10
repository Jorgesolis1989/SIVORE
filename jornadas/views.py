from django.contrib.auth.decorators import permission_required

from django.shortcuts import render_to_response, render, redirect
from jornadas.forms import FormularioRegistroJornada, FormularioEditarJornada
from planchas.models import Plancha
from candidatos.models import Candidato

from corporaciones.models import Corporacion
from datetime import datetime
from django.utils import timezone

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
             # Creando la jornada electoral y habilitando las corporaciones.
            corporaciones = form.cleaned_data["corporaciones"]


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
            jornada.corporaciones = corporaciones

            try:
                jornada.save()
            except Exception as e:
                print(e)


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
   jornada_corporaciones = Jornada_Corporacion.objects.filter(jornada__is_active=True).values_list('corporacion_id', flat=True)
   llamarMensaje = request.session.pop('llamarMensaje', None)
   mensaje = request.session.pop('mensaje', None)
   return render(request,  'listar_jornadas.html', {'jornadas': jornadas, 'llamarMensaje': llamarMensaje,'mensaje': mensaje,
                                                    'jornada_corporaciones': jornada_corporaciones})

# funcion que permite la edición de la jornada seleccionada
@permission_required("usuarios.Administrador", login_url="/")
def editar_jornada(request, id):
    try:
        jornada = Jornada.objects.get(id = id)
    except Jornada.DoesNotExist:
        llamarmensaje = "fracaso_usuario"
        mensaje = "La jornada #" + str(id)+ " no existe en el sistema."
        request.session["llamarMensaje"] = llamarmensaje
        request.session["mensaje"] = mensaje
        return redirect("listar_jornadas")

    if request.method == 'POST' and "btncreate" in request.POST:
        form = FormularioEditarJornada(request.POST)
        #Si el formulario es valido

        if form.is_valid():
            jornada.nombrejornada =  form.cleaned_data["nombre_jornada"]

            hora_completa = form.cleaned_data["fecha_jornada"] + " " + form.cleaned_data["hora_inicio"]
            jornada.fecha_inicio_jornada = datetime.strptime(hora_completa, "%m/%d/%Y %I:%M %p")
            jornada.fecha_inicio_jornada = timezone.make_aware(jornada.fecha_inicio_jornada,
                                                               timezone.get_current_timezone())
            print(hora_completa)

            hora_completa = form.cleaned_data["fecha_jornada"] +   " "+  form.cleaned_data["hora_final"]
            jornada.fecha_final_jornada = datetime.strptime(hora_completa, "%m/%d/%Y %I:%M %p")
            jornada.fecha_final_jornada = timezone.make_aware(jornada.fecha_final_jornada,
                                                               timezone.get_current_timezone())

            print(jornada.fecha_final_jornada)

            # Creando la jornada electoral y habilitando las corporaciones.
            corporaciones = form.cleaned_data["corporaciones"]
            try:
                jornada.save()
            except Exception as e:
                print(e)

            # Trabajar con las corporaciones
            jornadas_activas = Jornada_Corporacion.objects.filter(jornada_id = jornada.id , is_active=True)


            for jornada_activa in jornadas_activas:
                # Verificando las corporaciones de la lista de jornadas
                if jornada_activa.corporacion not in corporaciones:

                    # Desactivamos los candidatos de esa jornada
                    candidatos_a_desactivar = Candidato.objects.filter(jornada_corporacion__jornada_id=jornada_activa.jornada.id ,
                                                                       jornada_corporacion__corporacion__id=jornada_activa.corporacion.id,
                                                                       is_active=True)
                    #Guardando los candidatos
                    for candidato in candidatos_a_desactivar:
                        candidato.is_active = False
                        candidato.save()

                    # Desactivamos las planchas de la jornada
                    planchas_a_desactivar = Plancha.objects.filter(jornada_corporacion__jornada_id=jornada_activa.jornada.id ,
                                                                       jornada_corporacion__corporacion__id=jornada_activa.corporacion.id,
                                                                       is_active=True)
                    #Guardando los planchas
                    for plancha in planchas_a_desactivar:
                        plancha.is_active = False
                        plancha.save()

                    # Desactivamos la jornada
                    jornada_activa.is_active = False
                    try:
                        jornada_activa.save()
                    except Exception as e:
                        print(e)

            #Para agregar las corporaciones faltantes
            for corporacion in corporaciones:
                if corporacion.id not in jornadas_activas.values_list('corporacion__id' , flat=True):
                    jornada_corporacion = Jornada_Corporacion(jornada=jornada , corporacion=corporacion , is_active=True)
                    try:
                        jornada_corporacion.save()
                    except Exception as e:
                        print(e)

                    ingresar_plancha_voto_blanco(jornada_corporacion)


            jornada.corporaciones = corporaciones
            try:
                jornada.save()
            except Exception as e:
                print(e)


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
        corporaciones_de_jornada = Corporacion.objects.filter(id__in=Jornada_Corporacion.objects.filter(jornada_id= jornada.id, is_active=True, ).values_list("corporacion__id" , flat=True))
        print(corporaciones_de_jornada)

        # lista de ids Corporaciones ocupadas
        corporaciones_ocupadas = Corporacion.objects.filter(id__in=Jornada_Corporacion.objects.filter(jornada__is_active=True).values_list("corporacion__id", flat=True))

        # Corporaciones libres
        corporaciones_libres= Corporacion.objects.all().exclude(id__in=corporaciones_ocupadas.exclude(id__in=corporaciones_de_jornada.values_list("id", flat=True)).values_list("id", flat=True))

        # Agregando las corporaciones de la jornada porque aparecen ocupadas
        form.fields["corporaciones"].queryset = corporaciones_libres

        #envio de datos al formulario editar
        form.initial = {'nombre_jornada' : jornada.nombrejornada, "fecha_jornada" : jornada.fecha_inicio_jornada.date().strftime("%m/%d/%Y"),
                        "hora_inicio" : timezone.localtime(jornada.fecha_inicio_jornada).strftime('%I:%M %p'),
                        "hora_final" : timezone.localtime(jornada.fecha_final_jornada).strftime('%I:%M %p'), "corporaciones": [o for o in corporaciones_de_jornada]}
    return render(request, 'editar_jornada.html', {'form': form})

# Este metodo no elimina en la base de datos, sino que desactiva la jornada con sus dependencias (Planchas y Candidatos)
@permission_required("usuarios.Administrador", login_url="/")
def eliminar_jornada(request, idjornada=None):
    if request.method == 'POST':
        # Desactivando la jornada de la tabla jornada
        jornada=Jornada.objects.get(id=idjornada , is_active=True)
        jornada.is_active = False
        try:
            jornada.save()
        except Exception as e:
            print(e)

        # Desactivando las planchas de la tabla Jornada_Corporacion
        planchas_jornada = Plancha.objects.filter(jornada_corporacion__jornada_id=idjornada , is_active=True)
        for plancha_jornada in planchas_jornada:
            plancha_jornada.is_active = False
            try:
                plancha_jornada.save()
            except Exception as e:
                print(e)

        # Desactivando los candidatos
        candidatos_jornada = Candidato.objects.filter(jornada_corporacion__jornada_id=idjornada , is_active=True)
        for candidato_jornada in candidatos_jornada:
            candidato_jornada.is_active = False
            try:
                candidato_jornada.save()
            except Exception as e:
                print(e)

        llamarMensaje = "elimino_corporacion"
        mensaje = "Se eliminó la jornada electoral  " +  str(jornada.nombrejornada) +" con sus candidatos y corporaciones asociadas sactisfactoriamente"
        request.session['llamarMensaje'] = llamarMensaje
        request.session['mensaje'] = mensaje
    return redirect("listar_jornadas")
