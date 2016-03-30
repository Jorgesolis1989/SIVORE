from django.shortcuts import render_to_response
from django.shortcuts import render ,redirect
from django.template.context import RequestContext
from corporaciones.models import Corporacion
from django.contrib.auth.decorators import permission_required
from corporaciones.forms import FormularioRegistroCorporacion, FormularioEditarCorporacion

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
            corporacion = Corporacion.objects.filter(id_corporation=id_corporation)

            print("Es Valido")

            #Si el usuario no existe, lo crea
            if not corporacion:
                # Creando corporacion
                corporacion = Corporacion()
                corporacion.id_corporation= form.cleaned_data["id_corporation"]
                corporacion.name_corporation= form.cleaned_data["name_corporation"]
                corporacion.facultad= form.cleaned_data["facultad"]

                #Crea corporacion en la BD s i hay excepcion
                try:
                    corporacion.save()
                except Exception as e:
                    print(e)

                form = FormularioRegistroCorporacion()
                llamarMensaje = "exito_corporacion"
                mensaje = "La corporación "+ str(id_corporation)  +" se guardo correctamente"
            else:
                form = FormularioRegistroCorporacion()
                llamarMensaje = "fracaso_corporacion"
                mensaje = "La corporación " + str(id_corporation)  + " ya esta registrada"

            return render_to_response('registro_corporacion.html', {'mensaje': mensaje, 'form': form , "llamarMensaje": llamarMensaje}, context_instance=RequestContext(request))
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
    corporaciones = Corporacion.objects.all()
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


@permission_required("usuarios.Administrador", login_url="/")
def eliminar_corporacion(request, id_corporation=None):
    if request.method == 'POST':
        corporacion=Corporacion.objects.get(id_corporation=id_corporation)
        try:
            corporacion.delete()
        except Exception as e:
            print(e)
    llamarMensaje = "elimino_corporacion"
    mensaje = "Se eliminó la corporacion " +  str(id_corporation) +" sactisfactoriamente"
    request.session['llamarMensaje'] = llamarMensaje
    request.session['mensaje'] = mensaje

    return redirect("listar_corporacion")