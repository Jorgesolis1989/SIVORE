from django.shortcuts import render_to_response
from django.shortcuts import render
from django.template.context import RequestContext
from corporaciones.models import Corporacion
from django.contrib.auth.decorators import permission_required
from corporaciones.forms import FormularioRegistroCorporacion, FormularioEditarCorporacion

@permission_required("usuarios.Administrador" , login_url="/")
def registro_corporacion(request):
    mensaje = ""
    if request.method == 'POST':
        form = FormularioRegistroCorporacion(request.POST)

        #Si el formulario es valido y tiene datos
        if form.is_valid():
            #Capture el id de corporacion
            id_corporation = form.cleaned_data["id_corporation"]

            #Consultando la corporacion en la base de datos.
            corporacion = Corporacion.objects.filter(id_corporation=id_corporation)

            #Si el usuario no existe, lo crea
            if not corporacion:
                # Creando corporacion
                corporacion = Corporacion()
                corporacion.id_corporation= form.cleaned_data["id_corporation"]
                corporacion.name_corporation= form.cleaned_data["name_corporation"]
                corporacion.id_facultad= form.cleaned_data["id_facultad"]

                #Crea corporacion en la BD s i hay excepcion
                try:
                    corporacion.save()
                except Exception as e:
                    print(e)

                form = FormularioRegistroCorporacion()
                mensaje = "La corporación se guardo correctamente"
            else:
                form = FormularioRegistroCorporacion()
                mensaje = "La corporación " + str(id_corporation)  + " ya esta registrada"

            return render_to_response('registro_corporacion.html', {'mensaje': mensaje, 'form': form}, context_instance=RequestContext(request))
        else:
            form = FormularioRegistroCorporacion()
            data = {
                'form': form,
            }
            return render_to_response('registro_usuario.html', data, context_instance=RequestContext(request))
    else:
        form = FormularioRegistroCorporacion()

    return render(request, 'registro_corporacion.html',{'mensaje': mensaje, 'form': form})

# Vista para listar corporaciones
@permission_required("usuarios.Administrador", login_url="/")
def listar_corporacion(request):
    corporaciones = Corporacion.objects.all()
    return render(request, 'listar_corporaciones.html', {'corporaciones': corporaciones})

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
            corporacion.id_facultad = form.cleaned_data["id_facultad"]

             #Actualiza la corporacion en la BD si hay excepcion
            try:
                corporacion.save()
            except Exception as e:
                print(e)

            #Consultando la corporacion en la base de datos.
            return listar_corporacion(request)
    else:
        if id_corporation is None:
            return render(request, 'administrador.html')
        else:
            form = FormularioEditarCorporacion()

            form.initial = {'id_corporation': corporacion.id_corporation, 'name_corporation': corporacion.name_corporation, 'id_facultad': corporacion.id_facultad}
        return render(request, 'editar_corporacion.html', {'form': form})


@permission_required("usuarios.Administrador", login_url="/")
def eliminar_corporacion(request, id_corporation=None):
    if request.method == 'POST':
        corporacion=Corporacion.objects.get(id_corporation=id_corporation)
        try:
            corporacion.delete()
        except Exception as e:
            print(e)
    return listar_corporacion(request)