from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response, render, redirect
from jornadas.forms import FormularioRegistroJornada

from jornadas.models import Jornada , Jornada_Corporacion



@permission_required("usuarios.Administrador", login_url="/")
def registro_jornada(request):
    #Verificación para crear una jornada
    if request.method == 'POST' and  "btncreate" in request.POST:
        form = FormularioRegistroJornada(request.POST)
        #Si el formulario es valido
        print(form)
        if form.is_valid():
            print("form jornada valido")
            jornada = Jornada()
            jornada.nombre_jornada = form.cleaned_data["nombre_jornada"]
            jornada.fecha_inicio_jornada = form.cleaned_data["fecha_inicial"]
            jornada.fecha_final_jornada = form.cleaned_data["fecha_final"]
            try:
                jornada.save()
            except Exception as e:
                print(e)

            jornada_corporaciones = form.cleaned_data["corporaciones"]
            for corporacion in jornada_corporaciones:
                jornada_corporacion = Jornada_Corporacion()
                #guardamos jornada
                jornada_corporacion.jornada = jornada
                #guardamos corporacion
                jornada_corporacion.corporacion = corporacion
                try:
                    jornada_corporacion.save()
                except Exception as e:
                    print(e)
        #si no es valido el formulario, crear
        else:
            mensaje = "Datos incompleto para crear la jornada"
            llamarMensaje = "fracaso_usuario"
            form = FormularioRegistroJornada()
            data = {'mensaje': mensaje, 'form': form, 'llamarMensaje':llamarMensaje}
            return render(request, 'registro_jornada.html', data)

    else:
        form = FormularioRegistroJornada()
        return render(request, 'registro_jornada.html', {'form': form})

# Vista para listar votantes
@permission_required("usuarios.Administrador", login_url="/")
def listar_jornadas(request):
    corporaciones_jornada = Jornada_Corporacion.objects.filter(jornada__is_active=True)
    llamarMensaje = request.session.pop('llamarMensaje', None)
    mensaje = request.session.pop('mensaje', None)
    return render(request,  'listar_jornadas.html', {'corporaciones_jornada': corporaciones_jornada, 'llamarMensaje': llamarMensaje,'mensaje': mensaje})

