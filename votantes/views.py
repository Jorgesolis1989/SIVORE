from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response, redirect, render
from votantes.models import Votante
from usuarios.models import Usuario
from candidatos.models import Candidato
from planchas.models import Plancha
from django.db.models import Q
from corporaciones.models import Corporacion
from django.template.context import RequestContext
from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import permission_required
from votantes.forms import FormularioRegistroVotante, FormularioEditarVotante, FormularioCargar
import csv
from io import StringIO
from django.contrib.auth.models import User

#Vista de registro de usuarios
@permission_required("usuarios.Administrador", login_url="/")
def registro_votante(request):
    mensaje = ""
    llamarMensaje = ""

    #Verificación para crear un solo votante
    if request.method == 'POST' and "btncreate" in request.POST:
        form = FormularioRegistroVotante(request.POST)
        form2 = FormularioCargar()

        #Si el formulario es valido y tiene datos
        if form.is_valid():
            #Capture la cedula del votante
            cedula_votante = form.cleaned_data["cedula_usuario"]

            try:
                #Consultando el votante en la base de datos.
                votante = Votante.objects.get(usuario__cedula_usuario=cedula_votante)

            #Si el votante no existe, lo crea
            except Votante.DoesNotExist:
                # Creando el usuario votante
                usuario = Usuario()
                createuservotante(usuario, form)
                # Borrando los datos del formulario y enviando el mensaje de sactisfacion
                form = FormularioRegistroVotante()
                mensaje = "El votante se guardo correctamente, la contraseña se envío al correo " + usuario.email
                llamarMensaje = "exito_usuario"
            else:
                # Si el votante esta en la BD y no esta activo

                if not Usuario.is_active:
                    usuario = Usuario()
                    createuservotante(usuario, form)
                    mensaje = "El votante se guardo correctamente, la contraseña se envío al correo " + usuario.email
                    llamarMensaje = "exito_usuario"

                # Si el votante ya existe en la BD y esta activo
                else:
                    mensaje = "El votante " + str(cedula_votante)+ " ya esta registrado"
                    llamarMensaje = "fracaso_usuario"

            request.session['llamarMensaje'] = llamarMensaje
            request.session['mensaje'] = mensaje
            return redirect("listar_votantes")

        #si no es valido el formulario crear
        else:
            form = FormularioRegistroVotante()
            data = {
                'form': form,
                'form2':form2,
            }
            return render(request, 'registro_votante.html', data)

    #Verificación para cargar usuarios votantes
    elif request.method == 'POST' and "btnload" in request.POST:

        form = FormularioRegistroVotante()
        form2 = FormularioCargar(request.POST, request.FILES)
        crearVotante = False

        #Si el formulario es valido y tiene datos
        if form2.is_valid():
            csvf = StringIO(request.FILES['file'].read().decode())
            reader = csv.reader(csvf, delimiter=',')
            line=0
            useredit =0;
            usercreate=0;
            userexist=0;
            for row in reader:
                if (line > 0):
                    #Consultando el votante en la base de datos.
                    try:
                        usuario = Usuario.objects.get(cedula_usuario=row[0])
                    except Usuario.DoesNotExist:
                        usuario = Usuario()
                        usuario.cedula_usuario = row[0]
                        usuario.first_name = row[1]
                        usuario.last_name = row[2]
                        usuario.email = row[3]
                        usuario.username = row[0]
                        usuario.is_active = True
                        #generando el password aleatorio.
                        password = User.objects.make_random_password()
                        usuario.set_password(password)

                        votante = Votante()
                        votante.usuario = usuario
                        votante.codigo = row[4]
                        crearVotante = True
                        try:
                            plan = Corporacion.objects.get(id_corporation=row[5])
                            votante.plan = plan
                        except Corporacion.DoesNotExist:
                            mensaje = "ERROR el plan " + str(row[5]) + "No está creado en el sistema, debe de crearlo para continuar.... Votantes creados "+ str(usercreate)
                            llamarMensaje = "fracaso_usuario"
                            return render_to_response('registro_votante.html', {'mensaje': mensaje, 'form': form , 'form2':form2, 'llamarMensaje': llamarMensaje}, context_instance=RequestContext(request))


                        # Enviando contraseña al correo electronico registrado.
                        mensaje = "Señor(a) ", usuario.first_name , "\nSu usuario de acceso es: ", usuario.cedula_usuario , "\n Contraseña: ", usuario.password

                        #send_mail('Envío de contraseña de acceso a SIVORE', mensaje, 'sivoreunivalle@gmail.com', [usuario.email], fail_silently=False)
                        usercreate +=1

                    #Usuario ya existe pero esta desactivo
                    else:
                        if not usuario.is_active:
                            usuario.is_active = True
                            useredit +=1
                        else:
                            userexist +=1
                    #Crea el usuario en la BD s i hay excepcion
                    try:
                        usuario.save()
                    except Exception as e:
                        print(e)

                    #Crea el votante en la BD si hay excepcion
                    if crearVotante:
                        try:
                            votante.save()
                            crearVotante = False
                        except Exception as e:
                            print(e)

                    #Removiendo los permisos
                    for permission in usuario.user_permissions.all():
                        usuario.user_permissions.remove(permission)

                    # Poniendo el permiso de votante
                    usuario.user_permissions.add(Permission.objects.get(codename='Votante'))
                else:
                    line += 1

            mensaje = "Se crearon exitosamente " + str(usercreate) + " y se activaron " + str(useredit) + " votantes en el sistema."
            if userexist != 0:
                mensaje = mensaje + ", además estaba activos " + str(userexist) + " votantes."

            llamarMensaje = "exito_usuario"
            request.session['llamarMensaje'] = llamarMensaje
            request.session['mensaje'] = mensaje
            return redirect("listar_votantes")
    #Ninguno de los dos formularios crear  ni cargar Method GET
    else:
        form = FormularioRegistroVotante()
        form2 = FormularioCargar()
        return render_to_response('registro_votante.html',{'mensaje': mensaje, 'form': form, 'form2':form2, 'llamarMensaje': llamarMensaje}, context_instance=RequestContext(request))


# Vista para listar votantes
@permission_required("usuarios.Administrador", login_url="/")
def listar_votantes(request):
    votantes = Votante.objects.filter(usuario__is_active=True)
    llamarMensaje = request.session.pop('llamarMensaje', None)
    mensaje = request.session.pop('mensaje', None)
    varvotante ="votante"

    return render(request, 'listar_votantes.html', {'votantes': votantes,'llamarMensaje': llamarMensaje,'mensaje': mensaje, 'varvotante' : varvotante})


@permission_required("usuarios.Administrador", login_url="/")
def eliminar_votante(request, username=None):
    if request.method == 'POST':
        try:
            votante = Votante.objects.filter(usuario__cedula_usuario=username)

            if votante:
                votante[0].is_active = False
                votante[0].usuario.is_active = False
                votante[0].save()

                # Si tiene candidatp
                candidato = Candidato.objects.filter(votante= votante)
                if candidato:
                    candidato[0].is_active = False
                    candidato[0].save()

                    # Si tiene plancha
                    plancha = Plancha.objects.filter(Q(candidato_principal=candidato[0]) |
                                                     Q(candidato_suplente=candidato[0]))
                    if plancha:
                        plancha[0].is_active = False
                        plancha[0].save()


        except Exception as e:
            llamarMensaje = "fracaso_usuario"
            mensaje = "Hubo un eror, no se eliminó el votante " +  str(username) +" sactisfactoriamente."

        else:
        #redireccionando a la vista
            llamarMensaje = "elimino_usuario"
            mensaje = "Se eliminó el votante " +  str(username) +" sactisfactoriamente."

        request.session['llamarMensaje'] = llamarMensaje
        request.session['mensaje'] = mensaje
        return redirect("listar_votantes")

def createuservotante(usuario, form):
    usuario.cedula_usuario = form.cleaned_data["cedula_usuario"]
    usuario.first_name = form.cleaned_data["nombre_usuario"]
    usuario.last_name = form.cleaned_data["apellido_usuario"]
    usuario.email = form.cleaned_data["email"]
    usuario.username = form.cleaned_data["cedula_usuario"]
    usuario.is_active = True
    #generando el password aleatorio.
    password = User.objects.make_random_password()
    usuario.set_password(password)

    # Enviando contraseña al correo electronico registrado.
    mensaje = "Señor(a) ", usuario.first_name , "\nSu usuario de acceso es: ", usuario.cedula_usuario , "\n Contraseña: ", usuario.password
    #send_mail('Envío de contraseña de acceso a SIVORE', mensaje, 'sivoreunivalle@gmail.com', [usuario.email], fail_silently=False)

    #Crea el usuario en la BD s i hay excepcion
    try:
        usuario.save()
    except Exception as e:
        print(e)

    # Colocandole permisos al votante
    usuario.user_permissions.add(Permission.objects.get(codename='Votante'))

    #Creando en la tabla votante
    votante = Votante()
    votante.usuario = usuario
    votante.codigo = form.cleaned_data["codigo_estudiante"]
    votante.plan = form.cleaned_data["plan_estudiante"]

    #Crea el votante en la BD si hay excepcion
    try:
        votante.save()
    except Exception as e:
        print(e)