from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response, render, redirect
from django.db.models import Q
from planchas.models import Plancha

from django.template.context import RequestContext
import csv
from io import StringIO
from candidatos.models import Candidato
from votantes.models import Votante
from corporaciones.models import Corporacion
from candidatos.forms import FormularioRegistroCandidato, FormularioEditarCandidato
from jornadas.models import Jornada
from jornadas.models import Jornada_Corporacion

@permission_required("usuarios.Administrador", login_url="/")
def registro_candidato(request):

    #Verificación para crear un solo candidato

    if request.method == 'POST' and "btnload" in request.POST:
        form = FormularioRegistroCandidato(request.POST, request.FILES)

        #Si el formulario es valido y tiene datos
        if form.is_valid():

            #Capture la cedula del usuario
            votante = form.cleaned_data["votante"]

            candidato =Candidato.objects.filter(votante__usuario__cedula_usuario=votante.usuario.cedula_usuario)

            #Si el candidato no existe, lo crea
            if not candidato:
                # Creando el candidato
                candidato = Candidato()
                candidato.votante = votante
                candidato.tipo_candidato = form.cleaned_data["tipo_candidato"]
                candidato.jornada_corporacion = form.cleaned_data["corporacion"]

                # Foto del candidato
                if request.FILES:
                    candidato.foto = request.FILES['foto']
                else:
                    candidato.foto = None
                #Crea el usuario en la BD s i hay excepcion
                try:
                    candidato.save()
                except Exception as e:
                    print(e)

                mensaje = "El candidato " + str(votante.codigo)+ " fue creado exitosamente"
                llamarMensaje = "exito_usuario"
                request.session["llamarMensaje"] = llamarMensaje
                request.session["mensaje"] = mensaje
                return redirect("listar_candidatos")

            # Si el candidato ya existe en la BD
            else:
                form = FormularioRegistroCandidato()
                mensaje = "El candidato " + str(votante.codigo)+ " ya esta registrado en la base de datos"
                llamarMensaje = "fracaso_usuario"

            return render(request , 'registro_candidato.html', {'mensaje': mensaje, 'form': form, 'llamarMensaje':llamarMensaje})

        #si no es valido el formulario, crear
        else:
            mensaje = "El candidato no puede ser vacio"
            llamarMensaje = "fracaso_usuario"
            form = FormularioRegistroCandidato()
            data = {'mensaje': mensaje, 'form': form, 'llamarMensaje':llamarMensaje}
            return render(request, 'registro_candidato.html', data)

    elif request.POST:
        if not "votante" in request.POST:
            mensaje = "Por favor elegir un votante"
            llamarMensaje = "fracaso_usuario"
            form = FormularioRegistroCandidato()
            return render(request, 'registro_candidato.html', {'form': form, 'llamarMensaje':llamarMensaje , 'mensaje': mensaje})
        else:
            votante = Votante.objects.get(codigo=request.POST['votante'])
            form = FormularioRegistroCandidato(request.POST)

            corporaciones_habilitadas = Jornada_Corporacion.objects.filter(jornada__is_active=True)
            corporacion_candidato = corporaciones_habilitadas.filter(Q(corporacion__id_corporation=votante.plan.id_corporation) |
                                                                    Q(corporacion__id_corporation=votante.plan.facultad.id_corporation))

            form.fields["corporacion"].queryset = corporacion_candidato

    #Ninguno de los dos formularios crear  ni cargar Method GET
    else:
        form = FormularioRegistroCandidato()

        print(form.votantes_que_pueden_ser_candidatos)

        if not form.votantes_que_pueden_ser_candidatos:

            mensaje = "Debe de haber votantes para crear candidatos, dirijase a votantes"
            llamarMensaje = "fracaso_usuario"
            request.session["llamarMensaje"] = llamarMensaje
            request.session["mensaje"] = mensaje
            return redirect("listar_votantes")
        else:
            votante_inicial = form.votantes_que_pueden_ser_candidatos[0]
            form.fields["votante"].initial = votante_inicial


    return render(request, 'registro_candidato.html', {'form': form})

# Vista para listar votantes
@permission_required("usuarios.Administrador", login_url="/")
def listar_candidatos(request):
    candidatos = Candidato.objects.filter(is_active=True)
    llamarMensaje = request.session.pop('llamarMensaje', None)
    mensaje = request.session.pop('mensaje', None)

    return render(request,  'listar_candidatos.html', {'candidatos': candidatos, 'llamarMensaje': llamarMensaje,'mensaje': mensaje})


#Edicion candidato
@permission_required("usuarios.Administrador" , login_url="/")
def editar_candidato(request, codigo=None):
    try:
        candidato = Candidato.objects.get(votante__codigo=codigo)
    except Candidato.DoesNotExist:
        mensaje = "El candidato con codigo "+str(codigo)+" no existe"
        llamarMensaje = "fracaso_usuario"
        request.session["llamarMensaje"] = llamarMensaje
        request.session["mensaje"] = mensaje
        return redirect("listar_candidatos")

    if request.method == 'POST':
        form = FormularioEditarCandidato(request.POST)
        #Si el formulario es valido y tiene datos
        if form.is_valid():
            #Capture el codigo del candidato
            candidato.tipo_candidato = form.cleaned_data["tipo_candidato"]
            candidato.jornada_corporacion = form.cleaned_data["corporacion"]

            # Foto del candidato
            if request.FILES:
                candidato.foto = request.FILES['foto']

            print("entro hasta guara")
            #Actualiza  el usuario en la BD si hay excepcion
            try:
                candidato.save()
            except Exception as e:
                print(e)
            mensaje = "El candidato " + str(candidato.votante.codigo)+ " fue modifcado exitosamente."
            llamarMensaje = "exito_usuario"
            request.session["llamarMensaje"] = llamarMensaje
            request.session["mensaje"] = mensaje
            return redirect("listar_candidatos")
        else:
            if codigo is None:
                return render(request, 'administrador.html')
            else:
                form = FormularioEditarCandidato()

            return render(request, 'editar_candidato.html', {'form': form})
    else:
        form = FormularioEditarCandidato()

        try:
            votante = Votante.objects.get(codigo=codigo)
            candidato = Candidato.objects.get(votante__codigo=codigo)

            form.initial = {'votante': candidato.votante, 'nombrefoto': candidato.foto, 'tipo_candidato': candidato.tipo_candidato,
                           'corporacion' : candidato.jornada_corporacion}

            corporaciones_habilitadas = Jornada_Corporacion.objects.filter(jornada__is_active=True)
            corporacion_candidato = corporaciones_habilitadas.filter(Q(corporacion__id_corporation=votante.plan.id_corporation) |
                                                       Q(corporacion__id_corporation=votante.plan.facultad.id_corporation))

            form.fields["corporacion"].queryset = corporacion_candidato

        except Votante.DoesNotExist:
            print("Error")

        return render(request, 'editar_candidato.html', {'form': form})


@permission_required("usuarios.Administrador", login_url="/")
def eliminar_candidato(request, username=None):
    if request.method == 'POST':
        try:
            candidato=Candidato.objects.get(votante__codigo=username)
            candidato.is_active = False
            candidato.votante.is_active = False
            candidato.votante.usuario.is_active = False

            candidato.save()

            # if es candidato plancha
            plancha = Plancha.objects.filter(Q(candidato_principal=candidato) | Q(candidato_suplente=candidato))

            if plancha:
                print("encontre plancha")
                plancha[0].is_active = False
                plancha[0].save()

        except Exception:
            llamarMensaje = "fracaso_usuario"
            mensaje = "Hubo un error, no se eliminó el candidato " +  str(username)

        #redireccionando a la vista
        else:
            llamarMensaje = "elimino_usuario"
            mensaje = "Se eliminó el candidato " +  str(username) +" sactisfactoriamente"
        request.session['llamarMensaje'] = llamarMensaje
        request.session['mensaje'] = mensaje
        return redirect("listar_candidato")


