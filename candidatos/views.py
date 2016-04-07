from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response, render
from django.db.models import Q

from django.template.context import RequestContext
import csv
from io import StringIO
from candidatos.models import Candidato
from votantes.models import Votante
from usuarios.models import Usuario
from corporaciones.models import Corporacion
from candidatos.forms import FormularioRegistroCandidato, FormularioEditarCandidato

@permission_required("usuarios.Administrador", login_url="/")
def registro_candidato(request):

    #Verificación para crear un solo candidato

    if request.method == 'POST' and "btnload" in request.POST:
        form = FormularioRegistroCandidato(request.POST, request.FILES)

        #Si el formulario es valido y tiene datos
        if form.is_valid():

            print("es valido formulario candidato")
            #Capture la cedula del usuario
            votante = form.cleaned_data["votante"]

            candidato =Candidato.objects.filter(votante__usuario__cedula_usuario=votante.usuario.cedula_usuario)

            #Si el candidato no existe, lo crea
            if not candidato:
                # Creando el candidato
                candidato = Candidato()
                candidato.votante = votante
                candidato.tipo_candidato = form.cleaned_data["tipo_candidato"]
                candidato.corporacion = form.cleaned_data["corporacion"]

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

            # Si el candidato ya existe en la BD
            else:
                form = FormularioRegistroCandidato()
                mensaje = "El candidato " + str(votante.codigo)+ " ya esta registrado en la base de datos"
                llamarMensaje = "fracaso_usuario"

            return render(request , 'registro_candidato.html', {'mensaje': mensaje, 'form': form, 'llamarMensaje':llamarMensaje})

        #si no es valido el formulario, crear
        else:
            form = FormularioRegistroCandidato()
            data = {
                'form': form,
            }
            return render(request, 'registro_candidato.html', data)

    elif request.POST:
        form = FormularioRegistroCandidato()
        if not "votante" in request.POST:
            mensaje = "ERROR NO eligió ningún votante"
            llamarMensaje = "fracaso_usuario"
            return render(request, 'registro_candidato.html', {'form': form, 'llamarMensaje':llamarMensaje , 'mensaje': mensaje})

        else:
            votante = Votante.objects.get(codigo=request.POST['votante'])
            form.fields["corporacion"].queryset = Corporacion.objects.filter(Q(id_corporation=votante.plan.id_corporation) | Q(id_corporation=votante.plan.facultad.id_corporation))
        #print(form)

    #Ninguno de los dos formularios crear  ni cargar Method GET
    else:
        form = FormularioRegistroCandidato()
        votantes = Votante.objects.exclude(codigo__in=Candidato.objects.all().values_list('votante__codigo', flat=True))

        if not votantes:
            mensaje = "Debe de haber votantes para crear candidatos, dirijase a votantes"
            llamarMensaje = "fracaso_usuario"
            return render(request, 'registro_candidato.html', {'form': form, 'llamarMensaje':llamarMensaje , 'mensaje': mensaje})
        else:
            form.fields["votante"].initial = votantes[0]
            form.fields["corporacion"].queryset = Corporacion.objects.filter(Q(id_corporation=votantes[0].plan.id_corporation) | Q(id_corporation=votantes[0].plan.facultad.id_corporation))

    return render(request, 'registro_candidato.html', {'form': form})

# Vista para listar votantes
@permission_required("usuarios.Administrador", login_url="/")
def listar_candidatos(request):
    candidatos = Candidato.objects.all()
    llamarMensaje = request.session.pop('llamarMensaje', None)
    mensaje = request.session.pop('mensaje', None)

    return render(request,  'listar_candidatos.html', {'candidatos': candidatos, 'llamarMensaje': llamarMensaje,'mensaje': mensaje})


#Edicion candidato
@permission_required("usuarios.Administrador" , login_url="/")
def editar_candidato(request, codigo=None):
    candidato = Candidato.objects.get(votante__codigo=codigo)

    if request.method == 'POST':
        form = (request.POST)
        #Si el formulario es valido y tiene datos
        if form.is_valid():

            #Capture el codigo del candidato
            candidato.votante.codigo = form.cleaned_data["codigo_candidato"]
            candidato.votante.usuario.first_name = form.cleaned_data["nombres_candidato"]
            candidato.votante.usuario.last_name = form.cleaned_data["apellidos_candidato"]
            candidato.corporacion = form.cleaned_data["corporacion"]

             #Actualiza  el usuario en la BD si hay excepcion
            try:
                candidato.save()
            except Exception as e:
                print(e)
        else:
            if codigo is None:
                return render(request, 'administrador.html')

            else:
                form = FormularioEditarCandidato()

            return render(request, 'registro_candidato.html', {'form': form})

        return render(request, 'listar_candidatos.html', {'form': form})




