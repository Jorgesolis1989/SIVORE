from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response, render, redirect
from jornadas.forms import FormularioRegistroJornada
from planchas.models import Plancha
from candidatos.models import Candidato
from votantes.models import Votante
from usuarios.models import Usuario
from corporaciones.models import Corporacion

from jornadas.models import Jornada , Jornada_Corporacion



@permission_required("usuarios.Administrador", login_url="/")
def registro_jornada(request):
    #Verificación para crear una jornada
    if request.method == 'POST' and  "btncreate" in request.POST:
        form = FormularioRegistroJornada(request.POST)
        #Si el formulario es valido
        print(form)
        if form.is_valid():
            jornada = Jornada()
            jornada.nombre_jornada = form.cleaned_data["nombre_jornada"]
            jornada.fecha_inicio_jornada = form.cleaned_data["fecha_inicial"]
            jornada.fecha_final_jornada = form.cleaned_data["fecha_final"]
            try:
                jornada.save()
            except Exception as e:
                print(e)
            # Creando la jornada electoral y habilitando las corporaciones.
            jornada_corporaciones = form.cleaned_data["corporaciones"]
            for jornada_corporacion in jornada_corporaciones:
                jornada_corporacion = Jornada_Corporacion()
                #guardamos jornada
                jornada_corporacion.jornada = jornada
                #guardamos corporacion
                jornada_corporacion.corporacion = jornada_corporacion
                try:
                    jornada_corporacion.save()
                except Exception as e:
                    print(e)

                # Ingresando candidato voto en blanco a la corporacion a elegir
                ingresar_candidato_voto_blanco(jornada_corporacion)

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


def ingresar_candidato_voto_blanco(jornada_corporacion):
    """
    TODA CORPORACION DEBE DE TENER UNA PLANCHA VOTO EN BLANCO, ESTA SE CREA CUANDO SE CREA LA CORPORACIÓN
    """

    #Luego obtenemos el candidato voto en blanco
    try:
        candidato_voto_en_blanco = Candidato.objects.get(votante__codigo=0 )
    except Candidato.DoesNotExist:
     # Luego se busca el votante con ese codigo
        try:
            votante = Votante.objects.get(usuario__cedula_usuario=0)
        except Votante.DoesNotExist:

            # Primero buscamos la corporación voto en blanco
            try:
                corporacion_voto_blanco = Corporacion.objects.get(id_corporation=0)
            except Corporacion.DoesNotExist:
                corporacion_voto_blanco = Corporacion()
                corporacion_voto_blanco.id_corporation = 0
                corporacion_voto_blanco.is_active = False
                corporacion_voto_blanco.name_corporation =  "Corporacion para voto en blanco"

                try:
                    corporacion_voto_blanco.save()
                except Exception as e:
                    print(e)

            # Se procede a crear el usuario votante voto en blanco
            usuario = Usuario()
            usuario.cedula_usuario = 0
            usuario.username = 0
            usuario.first_name = "Voto en Blanco"
            usuario.is_active = False
            try:
                usuario.save()
            except Exception as e:
                print(e)

            votante = Votante()
            votante.usuario = usuario
            votante.codigo = 0
            votante.plan = corporacion_voto_blanco

            try:
                votante.save()
            except Exception as e:
                print(e)

            # Creando el candidato voto en blanco
            candidato_voto_en_blanco = Candidato()
            candidato_voto_en_blanco.corporacion =corporacion_voto_blanco
            candidato_voto_en_blanco.is_active = False
            candidato_voto_en_blanco.tipo_candidato = "Principal"
            candidato_voto_en_blanco.votante = votante

    # Guardando el candidato voto en blanco.
    try:
        candidato_voto_en_blanco.save()
    except Exception as e:
        print(e)

    # Creando la plancha con el candidato voto en blanco para esa corporacion especifica
    plancha_voto_en_blanco = Plancha()
    plancha_voto_en_blanco.candidato_principal = candidato_voto_en_blanco
    plancha_voto_en_blanco.is_active = True
    plancha_voto_en_blanco.jornada_corporacion = jornada_corporacion
    plancha_voto_en_blanco.numeroplancha = 0
    try:
        plancha_voto_en_blanco.save()
    except Exception as e:
        print(e)

