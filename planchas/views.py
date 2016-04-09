from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response, render, redirect
from django.db.models import Q
from candidatos.models import Candidato
from votantes.models import Votante
from corporaciones.models import Corporacion
from planchas.models import Plancha
from planchas.forms import FormularioRegistroPlancha, FormularioEditarPlancha

@permission_required("usuarios.Administrador", login_url="/")
def registro_plancha(request):

    #Verificación para crear un solo candidato

    if request.method == 'POST' and "btnload" in request.POST:
        form = FormularioRegistroPlancha(request.POST)

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
                request.session["llamarMensaje"] = llamarMensaje
                request.session["mensaje"] = mensaje
                return redirect("listar_planchas")

            # Si el candidato ya existe en la BD
            else:
                form = FormularioRegistroPlancha()
                mensaje = "El candidato " + str(votante.codigo)+ " ya esta registrado en la base de datos"
                llamarMensaje = "fracaso_usuario"

            return render(request , 'registro_plancha.html', {'mensaje': mensaje, 'form': form, 'llamarMensaje':llamarMensaje})

        #si no es valido el formulario, crear
        else:
            form = FormularioRegistroPlancha()
            data = {
                'form': form,
            }
            return render(request, 'registro_plancha.html', data)

    elif request.POST:
        form = FormularioRegistroPlancha()
        if not "votante" in request.POST:
            mensaje = "ERROR NO eligió ningún votante"
            llamarMensaje = "fracaso_usuario"
            return render(request, 'registro_plancha.html', {'form': form, 'llamarMensaje':llamarMensaje , 'mensaje': mensaje})

        else:
            votante = Votante.objects.get(codigo=request.POST['votante'])
            form.fields["corporacion"].queryset = Corporacion.objects.filter(Q(id_corporation=votante.plan.id_corporation) | Q(id_corporation=votante.plan.facultad.id_corporation))

    #Ninguno de los dos formularios crear  ni cargar Method GET
    else:
        form = FormularioRegistroPlancha()
        votantes = Votante.objects.exclude(codigo__in=Candidato.objects.all().values_list('votante__codigo', flat=True))

        if not votantes:
            mensaje = "Debe de haber votantes para crear candidatos, dirijase a votantes"
            llamarMensaje = "fracaso_usuario"
            return render(request, 'registro_plancha.html', {'form': form, 'llamarMensaje':llamarMensaje , 'mensaje': mensaje})
        else:
            form.fields["votante"].initial = votantes[0]
            form.fields["corporacion"].queryset = Corporacion.objects.filter(Q(id_corporation=votantes[0].plan.id_corporation) | Q(id_corporation=votantes[0].plan.facultad.id_corporation))

    return render(request, 'registro_plancha.html', {'form': form})

# Vista para listar votantes
@permission_required("usuarios.Administrador", login_url="/")
def listar_planchas(request):
    candidatos = Candidato.objects.all()
    llamarMensaje = request.session.pop('llamarMensaje', None)
    mensaje = request.session.pop('mensaje', None)

    return render(request,  'listar_planchas.html', {'candidatos': candidatos, 'llamarMensaje': llamarMensaje,'mensaje': mensaje})


#Edicion candidato
@permission_required("usuarios.Administrador" , login_url="/")
def editar_plancha(request, codigo=None):
    candidato = Candidato.objects.get(votante__codigo=codigo)

    if request.method == 'POST':
        form = FormularioEditarPlancha(request.POST)
        #Si el formulario es valido y tiene datos
        if form.is_valid():
            #Capture el codigo del candidato
            candidato.tipo_candidato = form.cleaned_data["tipo_candidato"]
            candidato.corporacion = form.cleaned_data["corporacion"]

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
                form = FormularioEditarPlancha()

            return render(request, 'registro_plancha.html', {'form': form})
    else:
        form = FormularioEditarPlancha()

        try:
            votante = Votante.objects.get(codigo=codigo)
            candidato = Candidato.objects.get(votante__codigo=codigo)
            print(candidato.foto)

            form.initial = {'votante': candidato.votante, 'nombrefoto': candidato.foto, 'tipo_candidato': candidato.tipo_candidato,
                           'corporacion' : candidato.corporacion}
            form.fields["corporacion"].queryset = Corporacion.objects.filter(Q(id_corporation=candidato.votante.plan.id_corporation) | Q(id_corporation=candidato.votante.plan.facultad.id_corporation))


        except Candidato.DoesNotExist:
            print("no existe")
        return render(request, 'editar_plancha.html', {'form': form})




