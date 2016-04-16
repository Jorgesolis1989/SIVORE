from django.shortcuts import render_to_response
from django.shortcuts import render ,redirect
from django.template.context import RequestContext
from corporaciones.models import Corporacion
from django.contrib.auth.decorators import permission_required
from corporaciones.forms import FormularioRegistroCorporacion, FormularioEditarCorporacion
from votantes.models import Votante
from planchas.models import Plancha
from candidatos.models import Candidato
from usuarios.models import Usuario
from django.db.models import Q

@permission_required("usuarios.Administrador" , login_url="/")
def registro_corporacion(request):
    mensaje = ""
    if request.method == 'POST':
        form = FormularioRegistroCorporacion(request.POST)
        print("Es Post")

        #Si el formulario es valido y tiene datos
        if form.is_valid():
            #Capture el id de corporacion
            id_corporation = form.cleaned_data["id_corporation"]

            #Consultando la corporacion en la base de datos.
            try:
                corporacion = Corporacion.objects.get(id_corporation=id_corporation)
            except Corporacion.DoesNotExist:
                corporacion = Corporacion()
                corporacion_create(corporacion, form)

                llamarMensaje = "exito_corporacion"
                mensaje = "La corporación "+ str(id_corporation)  +" se guardo correctamente"

            else:
                if not corporacion.is_active:
                    corporacion_create(corporacion, form)
                    llamarMensaje = "exito_corporacion"
                    mensaje = "La corporación "+ str(id_corporation)  +" se guardo correctamente"
                else:
                    llamarMensaje = "fracaso_corporacion"
                    mensaje = "La corporación " + str(id_corporation)  + " ya esta registrada"

            request.session['llamarMensaje'] = llamarMensaje
            request.session['mensaje'] = mensaje

            return redirect("listar_corporacion")
        else:
            form = FormularioRegistroCorporacion()
            data = {
                'form': form,
            }
            return render_to_response('registro_corporacion.html', data, context_instance=RequestContext(request))
    else:
        form = FormularioRegistroCorporacion()

    return render(request, 'registro_corporacion.html',{'mensaje': mensaje, 'form': form})

# Vista para listar corporaciones
@permission_required("usuarios.Administrador", login_url="/")
def listar_corporacion(request):

    llamarMensaje = request.session.pop('llamarMensaje', None)
    mensaje = request.session.pop('mensaje', None)
    corporaciones = Corporacion.objects.filter(is_active=True)
    return render(request, 'listar_corporaciones.html', {'corporaciones': corporaciones , 'llamarMensaje': llamarMensaje,'mensaje':mensaje })

#Edicion usuarios
@permission_required("usuarios.Administrador" , login_url="/")
def editar_corporacion(request, id_corporation=None):
    corporacion = Corporacion.objects.get(id_corporation=id_corporation)
    if request.method == 'POST':
        form = FormularioEditarCorporacion(request.POST)
        #Si el formulario es valido y tiene datos
        if form.is_valid():
            #Capture el id de corporacion
            corporacion.id_corporation = form.cleaned_data["id_corporation"]
            corporacion.name_corporation = form.cleaned_data["name_corporation"]
            corporacion.facultad = form.cleaned_data["facultad"]


             #Actualiza la corporacion en la BD si hay excepcion
            try:
                corporacion.save()
            except Exception as e:
                print(e)

            #Consultando la corporacion en la base de datos.
            llamarMensaje = "edito_corporacion"
            mensaje = "Se editó la corporacion " +  str(corporacion.id_corporation) +" sactisfactoriamente"
            request.session['llamarMensaje'] = llamarMensaje
            request.session['mensaje'] = mensaje

            return redirect("listar_corporacion")
    else:
        if id_corporation is None:
            return render(request, 'administrador.html')
        else:
            form = FormularioEditarCorporacion()

            form.initial = {'id_corporation': corporacion.id_corporation, 'name_corporation': corporacion.name_corporation, 'facultad': corporacion.facultad}
        return render(request, 'editar_corporacion.html', {'form': form})


# Este metodo no elimina en la base de datos, sino que desactiva la corporacion
@permission_required("usuarios.Administrador", login_url="/")
def eliminar_corporacion(request, id_corporation=None):
    if request.method == 'POST':
        corporacion=Corporacion.objects.get(id_corporation=id_corporation)

        # sacando los votantes de la corporacion
        votantes_corporacion = Votante.objects.filter((Q(plan__facultad__id_corporation=corporacion.id_corporation) |  Q(plan__id_corporation=corporacion.id_corporation)) & Q(is_active=True))

        # Si la corporacion tiene votantes
        if votantes_corporacion:
            llamarMensaje = "fracaso_usuario"
            mensaje = "No se eliminó la corporacion " +  str(id_corporation) +" porque tiene votantes asociados"

        else:
            corporacion.is_active = False

            llamarMensaje = "exito_usuario"
            mensaje = "Se eliminó la corporacion " +  str(id_corporation) +" sactisfactoriamente"

        try:
            corporacion.save()
        except Exception as e:
            print(e)

    request.session['llamarMensaje'] = llamarMensaje
    request.session['mensaje'] = mensaje

    return redirect("listar_corporacion")

def corporacion_create(corporacion, form):
    corporacion.id_corporation= form.cleaned_data["id_corporation"]
    corporacion.name_corporation= form.cleaned_data["name_corporation"]
    corporacion.facultad= form.cleaned_data["facultad"]
    corporacion.is_active = True

    try:
        corporacion.save()
    except Exception as e:
        print(e)


    """

    TODA CORPORACION DEBE DE TENER UNA PLANCHA VOTO EN BLANCO, ESTA SE CREA CUANDO SE CREA LA CORPORACIÓN
    """

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


    #Obteniendo candidato voto en blanco
    try:
        candidato_voto_en_blanco = Candidato.objects.get(votante__codigo=0 )
    except Candidato.DoesNotExist:
        """
        Esta operación se hará solo una vez si el usuario voto en blanco no existe en la base de datos
        """
        # Luego se busca el votante con ese codigo
        try:
            votante = Votante.objects.get(usuario__cedula_usuario=0)
        except Votante.DoesNotExist:
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

        candidato_voto_en_blanco = Candidato()
        candidato_voto_en_blanco.corporacion =corporacion_voto_blanco
        candidato_voto_en_blanco.is_active = False
        candidato_voto_en_blanco.tipo_candidato = "Principal"
        candidato_voto_en_blanco.votante = votante

        try:
            candidato_voto_en_blanco.save()
        except Exception as e:
            print(e)

    # Creando la plancha con el candidato voto en blanco
    plancha_voto_en_blanco = Plancha()
    plancha_voto_en_blanco.candidato_principal = candidato_voto_en_blanco
    plancha_voto_en_blanco.is_active = True
    plancha_voto_en_blanco.corporacion = corporacion
    plancha_voto_en_blanco.numeroplancha = 0
    try:
        plancha_voto_en_blanco.save()
    except Exception as e:
        print(e)