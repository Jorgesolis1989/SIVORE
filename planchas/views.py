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

    #Verificación para crear una plancha

    if request.method == 'POST' and "btnload" in request.POST:
        form = FormularioRegistroPlancha(request.POST)
        #Si el formulario es valido y tiene datos
        if form.is_valid():
            #Capture el numero de plancha
            numplancha = form.cleaned_data["numeroplancha"]

            plancha = Plancha.objects.filter(numeroplancha=numplancha)

            #Si la plancha no existe, la crea
            if not plancha:
                # Creando la plancha
                plancha = Plancha()
                plancha.numeroplancha = form.cleaned_data["numeroplancha"]
                plancha.corporacion = form.cleaned_data["corporacion"]
                plancha.candidato_principal = form.cleaned_data["candidato_principal"]
                plancha.candidato_suplente = form.cleaned_data["candidato_suplente"]

                try:
                    plancha.save()
                except Exception as e:
                    print(e)

                mensaje = "La plancha N° " + str(plancha.numeroplancha)+ " fue creada exitosamente."
                llamarMensaje = "exito_usuario"
                request.session["llamarMensaje"] = llamarMensaje
                request.session["mensaje"] = mensaje
                return redirect("listar_planchas")

            # Si la plancha ya existe en la BD
            else:
                form = FormularioRegistroPlancha()
                mensaje = "La plancha " + str(numplancha) + " ya esta existe."
                llamarMensaje = "fracaso_usuario"

            return render(request, 'registro_plancha.html', {'mensaje': mensaje, 'form': form, 'llamarMensaje':llamarMensaje})

        #si no es valido el formulario, crear
        else:
            form = FormularioRegistroPlancha()
            data = {
                'form': form,
            }
            return render(request, 'registro_plancha.html', data)

    # Cambio de corporacion
    elif request.POST:
        form = FormularioRegistroPlancha(request.POST)

        # Corporacion es nula
        if not "corporacion" in request.POST:
            mensaje = "Por favor elegir una corporación"
            llamarMensaje = "fracaso_usuario"
            return render(request, 'registro_plancha.html', {'form': form, 'llamarMensaje':llamarMensaje , 'mensaje': mensaje})

        # Cambio de corporacion y cargar candidatos de esa corporacion
        else:
            corporacion = Corporacion.objects.get(id_corporation=request.POST['corporacion'])
            form.fields["candidato_principal"].queryset = Candidato.objects.filter(Q(corporacion__id_corporation=corporacion.id_corporation) & Q (tipo_candidato='Principal'))
            form.fields["candidato_suplente"].queryset = Candidato.objects.filter(Q(corporacion__id_corporation=corporacion.id_corporation) & Q (tipo_candidato='Suplente'))

    #Ninguno de los dos formularios crear  ni cargar Method GET
    else:
        print("entre eee")
        form = FormularioRegistroPlancha()
        corporaciones = Corporacion.objects.all()

        if not corporaciones:
            mensaje = "Debe de haber corporaciones para crear las planchas, dirijase a corporaciones"
            llamarMensaje = "fracaso_usuario"
            return render(request, 'registro_plancha.html', {'form': form, 'llamarMensaje':llamarMensaje , 'mensaje': mensaje})
        else:
            #form.fields["corporacion"].initial = corporaciones[0]
            print(corporaciones[0])
            form.fields["candidato_principal"].queryset = Candidato.objects.filter(Q(corporacion =corporaciones[0].id_corporation) & Q(tipo_candidato="Principal"))
            form.fields["candidato_suplente"].queryset = Candidato.objects.filter(Q(corporacion=corporaciones[0].id_corporation) & Q(tipo_candidato="Suplente"))

    return render(request, 'registro_plancha.html', {'form': form})

# Vista para listar votantes
@permission_required("usuarios.Administrador", login_url="/")
def listar_planchas(request):
    planchas = Plancha.objects.all()
    llamarMensaje = request.session.pop('llamarMensaje', None)
    mensaje = request.session.pop('mensaje', None)

    return render(request,  'listar_planchas.html', {'planchas': planchas, 'llamarMensaje': llamarMensaje,'mensaje': mensaje})


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




