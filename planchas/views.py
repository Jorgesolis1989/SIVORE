from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response, render, redirect
from django.db.models import Q
from candidatos.models import Candidato
from votantes.models import Votante
from corporaciones.models import Corporacion
from jornadas.models import Jornada_Corporacion
from planchas.models import Plancha
from planchas.forms import FormularioRegistroPlancha, FormularioEditarPlancha
from itertools import chain



def plancha_create(plancha, form):
    #Capture el numero de plancha y candidato principal y suplente dados desde el form
    numplancha = form.cleaned_data["numeroplancha"]
    candidatoprin = form.cleaned_data["candidato_principal"]
    candidatosupl = form.cleaned_data["candidato_suplente"]
    jornada_corporacion = form.cleaned_data["jornada_corporacion"]
    url_plan_trabajo = form.cleaned_data["url_propuesta"]

    plancha.numeroplancha= numplancha
    plancha.jornada_corporacion= jornada_corporacion
    plancha.candidato_principal= candidatoprin
    plancha.candidato_suplente= candidatosupl
    plancha.is_active = True
    plancha.url_propuesta = url_plan_trabajo

    try:
        plancha.save()
    except Exception as e:
        print(e)

    jornada_corporacion.cantidad_planchas += 1

    try:
        jornada_corporacion.save()
    except Exception as e:
        print(e)


@permission_required("usuarios.Administrador", login_url="/")
def registro_plancha(request):
    #Verificación para crear una plancha
    disabledBtnnCrear = False

    if request.method == 'POST' and "btnload" in request.POST:
        form = FormularioRegistroPlancha(request.POST)

        #print("candidato principal " , form.cleaned_data["candidato_principal"])
        #Si el formulario es valido y tiene datos
        if form.is_valid():

            #Consulto en la BD si existen
            try:
                numplancha = form.cleaned_data["numeroplancha"]
                #plancha = Plancha.objects.filter(Q(numeroplancha=numplancha) & Q(jornada_corporacion=form.cleaned_data["jornada_corporacion"])
                #                                & Q(is_active=True))
                plancha = Plancha.objects.get(numeroplancha= numplancha, jornada_corporacion_id=form.cleaned_data["jornada_corporacion"], is_active=True)
                print("este es :",plancha)
            #Si la plancha no existe y los candidatos no estan asignados, crea la plancha
            except Plancha.DoesNotExist:
                # Creando la plancha
                plancha = Plancha()
                plancha_create(plancha, form)
                mensaje = "La plancha N° " + str(plancha.numeroplancha)+ " fue creada exitosamente."
                llamarMensaje = "exito_usuario"

            # Si la plancha ya existe en la BD
            else:
                if plancha.is_active:
                    mensaje = "La plancha" + str(numplancha) + " ya existe o los candidatos pertenecen a una plancha."
                    llamarMensaje = "fracaso_usuario"

                else:
                    plancha_create(plancha,form)
                    mensaje = "La plancha N° " + str(plancha.numeroplancha)+ " corporacion "+str(plancha.jornada_corporacion.corporacion.name_corporation)+" fue creada exitosamente."
                    llamarMensaje = "exito_usuario"

            request.session["llamarMensaje"] = llamarMensaje
            request.session["mensaje"] = mensaje
            return redirect("listar_planchas")

        #si no es valido el formulario, crear
        else:
            form = FormularioRegistroPlancha()
            llenarformplancha(form , form.jornada_corporaciones[0])
            mensaje = "No hay candidatos seleccionados para la corporación"
            llamarMensaje = "fracaso_usuario"
            return render(request,'registro_plancha.html', {'form':form, 'llamarMensaje':llamarMensaje, 'mensaje': mensaje})

    # Cambio de corporacion
    elif request.POST:
        form = FormularioRegistroPlancha(request.POST)

        # Corporacion es nula
        if not "jornada_corporacion" in request.POST:
            mensaje = "Por favor elegir una corporación habilitada a elegir"
            llamarMensaje = "fracaso_usuario"
            return render(request, 'registro_plancha.html', {'form': form, 'llamarMensaje':llamarMensaje, 'mensaje': mensaje})

        # Cambio de corporacion y cargar candidatos de esa corporacion
        else:
            jornada_corporacion =  request.POST['jornada_corporacion']
            llenarformplancha(form,jornada_corporacion)


    #Ninguno de los dos formularios crear  ni cargar Method GET
    else:
        form = FormularioRegistroPlancha()

        # Corporaciones que se van a elegir

        if not form.jornada_corporaciones:
            mensaje = "No hay corporaciones habilitadas para crear las planchas"
            llamarMensaje = "fracaso_usuario"
            disabledBtnCrear = True
            return render(request, 'registro_plancha.html', {'form': form, 'llamarMensaje':llamarMensaje , 'mensaje': mensaje , "disabledBtnCrear" : disabledBtnCrear})

        else:
            llenarformplancha(form, form.jornada_corporaciones[0])



    return render(request, 'registro_plancha.html', {'form': form, 'disabledBtnCrear': disabledBtnnCrear})

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
        plancha = Plancha.objects.get(jornada_corporacion__id=idcorporacion, numeroplancha=numplancha, is_active=True)
    except Plancha.DoesNotExist:
        # mensaje para redicionar si no existe la plancha de la URL
        mensaje = "La plancha" + str(numplancha) + " con jornada corporacion "+ str(idcorporacion)+" No existe en la BD "
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
                planchaBuscar = Plancha.objects.filter(jornada_corporacion__id=idcorporacion, numeroplancha=numeroplancha)

            #Si la plancha no existe y los candidatos no estan asignados, crea la plancha
            if not planchaBuscar:

                #Capture el numero de plancha y candidato principal y suplente dados desde el form
                plancha.numeroplancha = numeroplancha
                plancha.candidato_principal = form.cleaned_data["candidato_principal"]
                plancha.candidato_suplente = form.cleaned_data["candidato_suplente"]
                plancha.url_propuesta = form.cleaned_data["url_propuesta"]
                try:
                    plancha.save()
                except Exception as e:
                    print(e)

                mensaje = "La plancha #" + str(plancha.numeroplancha)+ "de la corporación "+ str(plancha.jornada_corporacion.corporacion)+" fue modificada exitosamente."
                llamarMensaje = "exito_usuario"

            # Si la plancha ya existe en la BD
            else:
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
        candidatos_a_excluir_principales = (Plancha.objects.filter(is_active=True , jornada_corporacion=plancha.jornada_corporacion)\
                                .exclude(Q(candidato_principal=None) | Q(candidato_principal__votante__codigo=plancha.candidato_principal.votante.codigo))).values_list('candidato_principal__votante__codigo')


        # Si la plancha tiene candidato suplente
        if plancha.candidato_suplente:
            """ Se debe de quitar la plancha con el voto en blanco es decir la plancha con candidato principak NONE"""

            # Los candidatos a excluir son los suplentes que se hallan lanzado a esa corporacion y que esten en alguna plancha activa
            #sacando a el de la plancha actual
            candidatos_a_excluir_suplentes = (Plancha.objects.filter(is_active=True, jornada_corporacion__corporacion__id=plancha.jornada_corporacion.corporacion.id)\
                                .exclude( Q(Q(candidato_suplente=None))| Q(candidato_suplente__votante__codigo=plancha.candidato_suplente.votante.codigo))).values_list('candidato_suplente__votante__codigo')

        else:
            # Si la plancha no tiene candidato suplente a excluir serían los suplentes de las otras planchas
            candidatos_a_excluir_suplentes = (Plancha.objects.filter(is_active=True , jornada_corporacion__corporacion__id=plancha.jornada_corporacion.corporacion.id).values_list('candidato_suplente__votante__codigo')).exclude(candidato_suplente__votante__codigo=None)

        candidatosprin_sin_plancha = Candidato.objects.filter(Q(jornada_corporacion__corporacion__id=plancha.jornada_corporacion.corporacion.id) & Q(tipo_candidato="Principal") & Q(is_active=True))\
        .exclude(votante__codigo__in=candidatos_a_excluir_principales)

        candidatossupl_sin_plancha = Candidato.objects.filter(Q(jornada_corporacion__corporacion__id=plancha.jornada_corporacion.corporacion.id) & Q(tipo_candidato="Suplente") & Q(is_active=True))\
        .exclude(votante__codigo__in=candidatos_a_excluir_suplentes)


        form.fields["candidato_principal"].queryset = candidatosprin_sin_plancha
        form.fields["candidato_suplente"].queryset = candidatossupl_sin_plancha

        try:
            form.initial = {'numeroplancha': plancha.numeroplancha, 'corporacion': plancha.jornada_corporacion,
                            'candidato_principal':plancha.candidato_principal, 'candidato_suplente':plancha.candidato_suplente,
                            'url_propuesta': plancha.url_propuesta}

        except Plancha.DoesNotExist:
            print("no existe plancha")

        return render(request, 'editar_plancha.html', {'form': form})

# Este metodo no elimina en la base de datos, sino que desactiva la corporacion
@permission_required("usuarios.Administrador", login_url="/")
def eliminar_plancha(request, idjornada=None, numplancha=None):
    if request.method == 'POST':
        plancha=Plancha.objects.get(jornada_corporacion__id=idjornada, numeroplancha = numplancha , is_active=True)
        plancha.is_active = False
        plancha.jornada_corporacion.cantidad_planchas -=1
        try:
            plancha.save()
        except Exception as e:
            print(e)

    llamarMensaje = "elimino_corporacion"
    mensaje = "Se eliminó la plancha #" + str(plancha.numeroplancha) +" de la corporacion "+ str(plancha.jornada_corporacion.corporacion.name_corporation)+" sactisfactoriamente"
    request.session['llamarMensaje'] = llamarMensaje
    request.session['mensaje'] = mensaje

    return redirect("listar_planchas")

def llenarformplancha(form , jornada_corporacion):
 # Candidatos principales y suplentes de la primera jornada_corporacion que esten activos
    candidatosprin_sin_plancha = Candidato.objects.filter(Q(jornada_corporacion_id=jornada_corporacion) & Q(tipo_candidato="Principal") & Q(is_active=True))
    candidatossupl_sin_plancha = (Candidato.objects.filter(Q(jornada_corporacion_id=jornada_corporacion) & Q(tipo_candidato="Suplente") & Q(is_active=True)))

    # Excluir a los candidatos principales que esten en una plancha
    candidatos_a_excluir_principales = Plancha.objects.filter(is_active=True).exclude(numeroplancha=0).values_list('candidato_principal__votante__codigo', flat=True)

    # Excluir a los candidatos suplentes que esten en una plancha
    candidatos_a_excluir_suplentes = Plancha.objects.filter(is_active=True).exclude(numeroplancha=0).values_list('candidato_suplente__votante__codigo', flat=True)


    candidatosprin_sin_plancha = candidatosprin_sin_plancha.exclude(votante__codigo__in= candidatos_a_excluir_principales)
    candidatossupl_sin_plancha = candidatossupl_sin_plancha.exclude(votante__codigo__in= candidatos_a_excluir_suplentes)

    form.fields["candidato_principal"].queryset = candidatosprin_sin_plancha
    form.fields["candidato_suplente"].queryset = candidatossupl_sin_plancha