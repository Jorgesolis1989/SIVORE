from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response, render
from django.template.context import RequestContext
import csv
from io import StringIO
from candidatos.models import Candidato
from votantes.models import Votante
from usuarios.models import Usuario
from corporaciones.models import Corporacion
from candidatos.forms import FormularioRegistroCandidato

@permission_required("usuarios.Administrador", login_url="/")
def registro_candidato(request):

    #Verificación para crear un solo usuario
    if request.method == 'POST':
        form = FormularioRegistroCandidato(request.POST)

        #Si el formulario es valido y tiene datos
        if form.is_valid():
            #Capture la cedula del usuario
            cedula_candidato = form.cleaned_data["cedula_candidato"]

            #Consultando el usuario en la base de datos.
            candidato = Candidato.objects.filter(cedula_candidato=cedula_candidato)

            #Si el candidato no existe, lo crea
            if not candidato:
                # Creando el candidato
                candidato = Candidato()
                candidato.cedula_candidato = cedula_candidato
                candidato.foto = form.cleaned_data["foto"]
                candidato.tipo_candidato = form.cleaned_data["tipo_candidato"]
                candidato.id_corporacion = form.cleaned_data["id_corporacion"]

                #Crea el usuario en la BD s i hay excepcion
                try:
                    candidato.save()
                except Exception as e:
                    print(e)

            # Si el candidato ya existe en la BD
            else:
                form = FormularioRegistroCandidato()
                mensaje = "El candidato " + str(cedula_candidato)+ " ya esta registrado"

            return render(request , 'registro_candidato.html', {'mensaje': mensaje, 'form': form})

        #si no es valido el formulario, crear
        else:
            form = FormularioRegistroCandidato()
            data = {
                'form': form,
            }
            return render(request, 'registro_candidato.html', data)

    #Ninguno de los dos formularios crear  ni cargar Method GET
    else:
        form = FormularioRegistroCandidato()
        candidato= Candidato()
        try:
            votantes = Votante.objects.all()
            print("ingresó view candidato")
            corporaciones = Corporacion.objects.all()
            print(votantes)
            form.initial = {'cedula_candidato': candidato.votante_candidato_id, 'tipo_candidato': candidato.tipo_candidato, 'corporacion': candidato.corporacion_candidato_id}
            print(form)
        except Votante.DoesNotExist:

            return render(request,'registro_candidato.html',{'form': form, 'votantes': votantes, 'corporaciones': corporaciones})

    return render_to_response('registro_candidato.html', {'form': form, 'votantes': votantes, 'corporaciones': corporaciones}, context_instance=RequestContext(request))




