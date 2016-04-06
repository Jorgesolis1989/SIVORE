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

    #Ninguno de los dos formularios crear  ni cargar Method GET
    else:
        form = FormularioRegistroCandidato()
    return render(request, 'registro_candidato.html', {'form': form})




