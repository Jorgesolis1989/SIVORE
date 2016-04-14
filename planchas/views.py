from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response, render, redirect
from django.db.models import Q
from candidatos.models import Candidato
from votantes.models import Votante
from corporaciones.models import Corporacion
from planchas.models import Plancha
from planchas.forms import FormularioRegistroPlancha, FormularioEditarPlancha
from itertools import chain

@permission_required("usuarios.Administrador", login_url="/")

def registro_plancha(request):
    #Verificación para crear una plancha
    if request.method == 'POST' and "btnload" in request.POST:
        form = FormularioRegistroPlancha(request.POST)
        #Si el formulario es valido y tiene datos
        if form.is_valid():

            #Consulto en la BD si existen
            try:
                numplancha = form.cleaned_data["numeroplancha"]
                plancha = Plancha.objects.get(numeroplancha= numplancha, corporacion=form.cleaned_data["corporacion"], is_active=True)

            #Si la plancha no existe y los candidatos no estan asignados, crea la plancha
            except Plancha.DoesNotExist:
                # Creando la plancha
                plancha = Plancha()
                plancha_create(plancha, form)
                mensaje = "La plancha N° " + str(plancha.numeroplancha)+ " fue creada exitosamente."
                llamarMensaje = "exito_usuario"

            # Si la plancha ya existe en la BD
            else:

                if not plancha.is_active:
                    mensaje = "La plancha" + str(numplancha) + " ya existe o los candidatos pertenecen a una plancha."
                    llamarMensaje = "fracaso_usuario"

                else:
                    plancha_create(plancha,form)
                    mensaje = "La plancha N° " + str(plancha.numeroplancha)+ " corporacion "+str(plancha.corporacion.name_corporation)+" fue creada exitosamente."
                    llamarMensaje = "exito_usuario"

            request.session["llamarMensaje"] = llamarMensaje
            request.session["mensaje"] = mensaje
            return redirect("listar_planchas")

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
            return render(request, 'registro_plancha.html', {'form': form, 'llamarMensaje':llamarMensaje, 'mensaje': mensaje})

        # Cambio de corporacion y cargar candidatos de esa corporacion
        else:
            corporacion = Corporacion.objects.get(id_corporation=request.POST['corporacion'])

            candidatosprin_sin_plancha = (Candidato.objects.filter(Q(corporacion=corporacion.id_corporation) & Q(tipo_candidato="Principal") & Q(is_active=True))).exclude(votante__codigo__in = Plancha.objects.filter(is_active=True).values_list('candidato_principal__votante__codigo', flat=True))

            candidatossupl_sin_plancha = (Candidato.objects.filter(Q(corporacion=corporacion.id_corporation) & Q(tipo_candidato="Suplente") & Q(is_active=True) )).exclude(votante__codigo__in = Plancha.objects.filter(is_active=True).values_list('candidato_suplente__votante__codigo', flat=True))

            form.fields["candidato_principal"].queryset = candidatosprin_sin_plancha
            form.fields["candidato_suplente"].queryset = candidatossupl_sin_plancha
    #Ninguno de los dos formularios crear  ni cargar Method GET
    else:
        form = FormularioRegistroPlancha()
        corporaciones = Corporacion.objects.all()

        if not corporaciones:
            mensaje = "Debe de haber corporaciones para crear las planchas, dirijase a corporaciones"
            llamarMensaje = "fracaso_usuario"
            return render(request, 'registro_plancha.html', {'form': form, 'llamarMensaje':llamarMensaje , 'mensaje': mensaje})
        else:

            # Candidatos principales de una corporacion que no estan en alguna plancha

            candidatosprin_sin_plancha = (Candidato.objects.filter(Q(corporacion=corporaciones[0].id_corporation) & Q(tipo_candidato="Principal") & Q(is_active=True))).exclude(corporacion__candidato__principal = Plancha.objects.filter(is_active=True).values_list('candidato_principal__votante__codigo', flat=True))

            candidatossupl_sin_plancha = (Candidato.objects.filter(Q(corporacion=corporaciones[0].id_corporation) & Q(tipo_candidato="Suplente") & Q(is_active=True) )).exclude(votante__codigo__in = Plancha.objects.filter(is_active=True).values_list('candidato_suplente__votante__codigo', flat=True))

            form.fields["candidato_principal"].queryset = candidatosprin_sin_plancha
            form.fields["candidato_suplente"].queryset = candidatossupl_sin_plancha

    return render(request, 'registro_plancha.html', {'form': form})

# Vista para listar votantes
@permission_required("usuarios.Administrador", login_url="/")
def listar_planchas(request):
    planchas = Plancha.objects.filter(is_active=True)
    llamarMensaje = request.session.pop('llamarMensaje', None)
    mensaje = request.session.pop('mensaje', None)

    return render(request,  'listar_planchas.html', {'planchas': planchas, 'llamarMensaje': llamarMensaje,'mensaje': mensaje})


#Edicion candidato
@permission_required("usuarios.Administrador" , login_url="/")
def editar_plancha(request, idcorporacion=None,numplancha=None):

    try:
        plancha = Plancha.objects.get(corporacion=idcorporacion, numeroplancha=numplancha)
    except Plancha.DoesNotExist:
        # mensaje para redicionar si no existe la plancha de la URL
        mensaje = "La plancha" + str(numplancha) + " con corporacion "+ str(idcorporacion)+" No existe en la BD "
        llamarMensaje = "fracaso_usuario"
        request.session["llamarMensaje"] = llamarMensaje
        request.session["mensaje"] = mensaje
        return redirect("listar_planchas")

    if request.method == 'POST' and "btnload" in request.POST:
        form = FormularioEditarPlancha(request.POST)

        #Si el formulario es valido y tiene datos
        if form.is_valid():


            numeroplancha = form.cleaned_data["numeroplancha"]

            #Consulto en la BD si existe la plancha
            if numeroplancha == int(numplancha):
                planchaBuscar = []
            else:
                planchaBuscar = Plancha.objects.filter(corporacion=idcorporacion, numeroplancha=numeroplancha)

            print(planchaBuscar)

            #Si la plancha no existe y los candidatos no estan asignados, crea la plancha
            if not planchaBuscar:

                #Capture el numero de plancha y candidato principal y suplente dados desde el form
                plancha.numeroplancha = numeroplancha
                plancha.candidato_principal = form.cleaned_data["candidato_principal"]
                plancha.candidato_suplente = form.cleaned_data["candidato_suplente"]

                try:
                    plancha.save()
                except Exception as e:
                    print(e)

                mensaje = "La plancha #" + str(plancha.numeroplancha)+ "de la corporación "+ str(plancha.corporacion)+" fue modificada exitosamente."
                llamarMensaje = "exito_usuario"

            # Si la plancha ya existe en la BD
            else:
                form = FormularioRegistroPlancha()
                mensaje = "La plancha " + str(numeroplancha) + " de la corporacion "+plancha.corporacion.name_corporation+" ya existe en el sistema"
                llamarMensaje = "fracaso_usuario"

            request.session["llamarMensaje"] = llamarMensaje
            request.session["mensaje"] = mensaje
            return redirect("listar_planchas")

        #si no es valido el formulario, crear
        else:
            form = FormularioEditarPlancha()
            data = {
                'form': form,
            }
            return render(request, 'editar_plancha.html', data)

    #Method GET
    else:
        form = FormularioEditarPlancha()

        # Candidatos principales y suplentes de una corporacion que no estan en alguna plancha

        # Todos los candidatos a excluir que ya estan en una plancha de la corporacion, menos el candidato principal actual
        candidatos_a_excluir_principales = (Plancha.objects.filter(is_active=True , corporacion__id_corporation=plancha.corporacion.id_corporation)\
                                .exclude(candidato_principal__votante__codigo=plancha.candidato_principal.votante.codigo)).values_list('candidato_principal__votante__codigo')

        if plancha.candidato_suplente:
            candidatos_a_excluir_suplentes = (Plancha.objects.filter(is_active=True , corporacion__id_corporation=plancha.corporacion.id_corporation)\
                                .exclude(candidato_suplente__votante__codigo=plancha.candidato_suplente.votante.codigo)).values_list('candidato_suplente__votante__codigo')
            print(candidatos_a_excluir_suplentes)
        else:
            candidatos_a_excluir_suplentes = (Plancha.objects.filter(is_active=True , corporacion__id_corporation=plancha.corporacion.id_corporation).values_list('candidato_suplente__votante__codigo')).exclude(candidato_suplente__votante__codigo=None)
            print("else")
            print(candidatos_a_excluir_suplentes)

        candidatosprin_sin_plancha = Candidato.objects.filter(Q(corporacion__id_corporation=plancha.corporacion.id_corporation) & Q(tipo_candidato="Principal") & Q(is_active=True))\
        .exclude(votante__codigo__in=candidatos_a_excluir_principales)

        candidatossupl_sin_plancha = Candidato.objects.filter(Q(corporacion__id_corporation=plancha.corporacion.id_corporation) & Q(tipo_candidato="Suplente") & Q(is_active=True))\
        .exclude(votante__codigo__in=candidatos_a_excluir_suplentes)


        form.fields["candidato_principal"].queryset = candidatosprin_sin_plancha
        form.fields["candidato_suplente"].queryset = candidatossupl_sin_plancha

        try:
            form.initial = {'numeroplancha': plancha.numeroplancha, 'corporacion': plancha.corporacion}

        except Plancha.DoesNotExist:
            print("no existe plancha")

        return render(request, 'editar_plancha.html', {'form': form})

# Este metodo no elimina en la base de datos, sino que desactiva la corporacion
@permission_required("usuarios.Administrador", login_url="/")
def eliminar_plancha(request, idcorporacion=None, numplancha=None):
    if request.method == 'POST':
        plancha=Plancha.objects.get(corporacion__id_corporation=idcorporacion, numeroplancha = numplancha )
        plancha.is_active = False
        try:
            plancha.save()
        except Exception as e:
            print(e)
    llamarMensaje = "elimino_corporacion"
    mensaje = "Se eliminó la plancha #" +  str(plancha.numeroplancha) +" de la corporacion "+ str(plancha.corporacion.name_corporation)+" sactisfactoriamente"
    request.session['llamarMensaje'] = llamarMensaje
    request.session['mensaje'] = mensaje

    return redirect("listar_planchas")

def plancha_create(plancha, form):


    #Capture el numero de plancha y candidato principal y suplente dados desde el form
    numplancha = form.cleaned_data["numeroplancha"]
    candidatoprin = form.cleaned_data["candidato_principal"]
    candidatosupl = form.cleaned_data["candidato_suplente"]
    corporacion = form.cleaned_data["corporacion"]

    plancha.numeroplancha= numplancha
    plancha.corporacion= corporacion
    plancha.candidato_principal= candidatoprin
    plancha.candidato_suplente= candidatosupl
    plancha.is_active = True



    try:
        plancha.save()
    except Exception as e:
        print(e)