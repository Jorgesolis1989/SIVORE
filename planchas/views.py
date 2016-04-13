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
    #plancha = Plancha.objects.filter(Q(corporacion=idcorporacion) & Q(numeroplancha=numplancha))
    #plancha = Plancha.objects.get(corporacion=idcorporacion, numeroplancha=numplancha)

    if request.method == 'POST' and "btnload" in request.POST:
        form = FormularioEditarPlancha(request.POST)
        #Si el formulario es valido y tiene datos
        if form.is_valid():

            #Consulto en la BD si existe la plancha
            plancha = Plancha.objects.filter(numeroplancha=numplancha)

            #Si la plancha no existe y los candidatos no estan asignados, crea la plancha
            if not plancha:
                #Capture el numero de plancha y candidato principal y suplente dados desde el form
                numplancha = form.cleaned_data["numeroplancha"]
                corporacion = form.cleaned_data["corporacion"]
                candidatoprin = form.cleaned_data["candidato_principal"]
                candidatosupl = form.cleaned_data["candidato_suplente"]

                try:
                    plancha.save()
                except Exception as e:
                    print(e)

                    mensaje = "La plancha #" + str(plancha.numeroplancha)+ "de la corporación "+ str(plancha.corporacion)+" fue modificada exitosamente."
                    llamarMensaje = "exito_usuario"
                    request.session["llamarMensaje"] = llamarMensaje
                    request.session["mensaje"] = mensaje
                    return redirect("listar_planchas")
            # Si la plancha ya existe en la BD
            else:
                form = FormularioRegistroPlancha()
                mensaje = "La plancha" + str(numplancha) + " ya existe o los candidatos pertenecen a una plancha."
                llamarMensaje = "fracaso_usuario"

            return render(request, 'registro_plancha.html', {'mensaje': mensaje, 'form': form, 'llamarMensaje':llamarMensaje})

        #si no es valido el formulario, crear
        else:
            form = FormularioEditarPlancha()
            data = {
                'form': form,
            }
            return render(request, 'editar_plancha.html', data)

    # Cambio de corporacion
    elif request.POST:
        form = FormularioEditarPlancha(request.POST)
        corporacion = Corporacion.objects.get(id_corporation=request.POST['corporacion'])
        candidatosprin_sin_plancha = (Candidato.objects.filter(Q(corporacion=corporacion.id_corporation) & Q(tipo_candidato="Principal") & Q(is_active=True))).exclude(votante__codigo__in = Plancha.objects.filter(is_active=True).values_list('candidato_principal__votante__codigo', flat=True))
        candidatossupl_sin_plancha = (Candidato.objects.filter(Q(corporacion=corporacion.id_corporation) & Q(tipo_candidato="Suplente") & Q(is_active=True) )).exclude(votante__codigo__in = Plancha.objects.filter(is_active=True).values_list('candidato_suplente__votante__codigo', flat=True))

        form.fields["candidato_principal"].queryset = candidatosprin_sin_plancha
        form.fields["candidato_suplente"].queryset = candidatossupl_sin_plancha

    #Ninguno de los dos formularios crear ni cargar Method GET
    else:
        form = FormularioEditarPlancha()
        corporaciones = Corporacion.objects.all()

        # Candidatos principales y suplentes de una corporacion que no estan en alguna plancha

        candidatosprin_sin_plancha = (Candidato.objects.filter(Q(corporacion=corporaciones[0].id_corporation) & Q(tipo_candidato="Principal") & Q(is_active=True))).exclude(corporacion__candidato__principal = Plancha.objects.filter(is_active=True).values_list('candidato_principal__votante__codigo', flat=True))

        candidatossupl_sin_plancha = (Candidato.objects.filter(Q(corporacion=corporaciones[0].id_corporation) & Q(tipo_candidato="Suplente") & Q(is_active=True) )).exclude(votante__codigo__in = Plancha.objects.filter(is_active=True).values_list('candidato_suplente__votante__codigo', flat=True))
        print("entre get en plancha")

        plancha = Plancha.objects.get(corporacion=idcorporacion, numeroplancha=numplancha)

        try:
            form.initial = {'numeroplancha': plancha.numeroplancha, 'corporacion': plancha.corporacion, 'candidato_principal': plancha.candidato_principal,
                            'candidato_suplente': plancha.candidato_suplente}

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