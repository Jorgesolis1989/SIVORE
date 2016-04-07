from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response, redirect, render
from django.template.context import RequestContext
import csv
from io import StringIO

from usuarios.models import Usuario
from votantes.models import Votante
from corporaciones.models import Corporacion

from usuarios.forms import FormularioLogin
from usuarios.forms import FormularioRegistroUsuario, FormularioEditarUsuario, FormularioCargar


#Método auxiliar para encontrar la vista del usuario
def retornar_vista(request, usuario):
    print(usuario.get_all_permissions())
    if usuario.has_perm("usuarios.Administrador"):
        return administrador_home(request, usuario)
    elif usuario.has_perm("usuarios.Votante"):
        return votante_home(request, usuario)
    elif usuario.has_perm("usuarios.Superior"):
        return superior_home(request, usuario)
    else:
        return login_view()
# Pagina principal para usuario Administrador
@permission_required("usuarios.Administrador" , login_url="/")
def administrador_home(request , usuario):
    return render(request, 'administrador.html', {'usuario': usuario})

# Pagina del home  para usuario Votante
@permission_required("usuarios.Votante" , login_url="/")
def votante_home(request, usuario):
    return render(request , 'votante.html', {'usuario': usuario})

# Pagina del home  para usuario Superior
@permission_required("usuarios.Superior" , login_url="/")
def superior_home(request, usuario):
    return render(request , 'superior.html', {'usuario': usuario})


#Pagina de login
def login_view(request):
    mensaje = ""
    if request.user.is_authenticated() and not request.user.is_superuser:
        usuario = Usuario.objects.get(username=request.user.username)
        return retornar_vista(request, usuario)

    elif request.method == 'POST':
        form = FormularioLogin(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            usuario = authenticate(username=cd['username'], password=cd['password'])
            if usuario is not None:
                if usuario.is_active:
                    login(request, usuario)

                    #Redireccionar
                    return retornar_vista(request, usuario)
                else:
                   mensaje = "Usuario no activado"
            else:
                   mensaje = "Datos erróneos. Por favor, inténtelo otra vez.    "
    else:
        form = FormularioLogin()
    return render(request, 'login.html', {'mensaje': mensaje, 'form': form })

#Vista de registro de usuarios
@permission_required("usuarios.Administrador", login_url="/")
def registro_usuario(request):
    mensaje = ""
    llamarMensaje = ""


    #Verificación para crear un solo usuario
    if request.method == 'POST' and "btncreate" in request.POST:
        form = FormularioRegistroUsuario(request.POST)
        form2 = FormularioCargar()

        #Si el formulario es valido y tiene datos
        if form.is_valid():
            #Capture la cedula del usuario
            cedula_usuario = form.cleaned_data["cedula_usuario"]

            #Consultando el usuario en la base de datos.
            usuario = Usuario.objects.filter(cedula_usuario=cedula_usuario)

            #Si el usuario no existe, lo crea
            if not usuario:
                # Creando el usuario
                usuario = Usuario()
                usuario.cedula_usuario = cedula_usuario
                usuario.first_name = form.cleaned_data["nombre_usuario"]
                usuario.last_name = form.cleaned_data["apellido_usuario"]
                usuario.email = form.cleaned_data["email"]
                usuario.username = cedula_usuario
                usuario.is_active = form.cleaned_data["esta_activo"]
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

                # Colocandole permisos al usuario
                usuario.user_permissions.add(Permission.objects.get(codename=form.cleaned_data["rol"]))

                 # Si es votante, Creando en la tabla votante
                if form.cleaned_data["rol"] == "Votante":
                    votante = Votante()
                    votante.usuario = usuario
                    votante.codigo = form.cleaned_data["codigo_estudiante"]
                    votante.plan = form.cleaned_data["plan_estudiante"]

                #Crea el votante en la BD si hay excepcion
                    try:
                        votante.save()
                    except Exception as e:
                        print(e)

                # Borrando los datos del formulario y enviando el mensaje de sactisfacion
                form = FormularioRegistroUsuario()
                mensaje = "El usuario se guardo correctamente, la contraseña se envío al correo " + usuario.email
                llamarMensaje = "exito_usuario"


            # Si el usuario ya existe en la BD
            else:
                form = FormularioRegistroUsuario()
                mensaje = "El usuario " + str(cedula_usuario)  + " ya esta registrado"
                llamarMensaje = "fracaso_usuario"


            return render(request, 'registro_usuario.html', {'mensaje': mensaje, 'form': form , 'form2':form2, 'llamarMensaje': llamarMensaje})

        #si no es valido el formulario crear
        else:
            form = FormularioRegistroUsuario()
            data = {
                'form': form,
                'form2':form2,
            }
            return render(request, 'registro_usuario.html', data)

    #Verificación para cargar usuarios votantes
    elif request.method == 'POST' and "btnload" in request.POST:

        form = FormularioRegistroUsuario()
        form2 = FormularioCargar(request.POST, request.FILES)
        crearVotante = False

        #Si el formulario es valido y tiene datos
        if form2.is_valid():
            csvf = StringIO(request.FILES['file'].read().decode())
            reader = csv.reader(csvf, delimiter=',')
            line=0
            useredit =0;
            usercreate=0;
            for row in reader:
                if (line > 0):
                    #Consultando el usuario en la base de datos.
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
                            return render_to_response('registro_usuario.html', {'mensaje': mensaje, 'form': form , 'form2':form2, 'llamarMensaje': llamarMensaje}, context_instance=RequestContext(request))


                        # Enviando contraseña al correo electronico registrado.
                        mensaje = "Señor(a) ", usuario.first_name , "\nSu usuario de acceso es: ", usuario.cedula_usuario , "\n Contraseña: ", usuario.password

                        #send_mail('Envío de contraseña de acceso a SIVORE', mensaje, 'sivoreunivalle@gmail.com', [usuario.email], fail_silently=False)
                        usercreate +=1

                    else:
                        usuario.is_active = True
                        useredit +=1
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

            mensaje = "Se crearon exitosamente " + str(usercreate) + " y se activaron " + str(useredit) + " votantes en el sistemas"
            llamarMensaje = "exito_usuario"
            request.session['llamarMensaje'] = llamarMensaje
            request.session['mensaje'] = mensaje
            return redirect("listar_usuario")
    #Ninguno de los dos formularios crear  ni cargar Method GET
    else:
        form = FormularioRegistroUsuario()
        form2 = FormularioCargar()
        return render_to_response('registro_usuario.html',{'mensaje': mensaje, 'form': form, 'form2':form2, 'llamarMensaje': llamarMensaje}, context_instance=RequestContext(request))

# Vista para listar usuarios
@permission_required("usuarios.Administrador" , login_url="/")
def listar_usuario(request):
    usuarios = Usuario.objects.all()
    llamarMensaje = request.session.pop('llamarMensaje', None)
    mensaje = request.session.pop('mensaje', None)

    return render(request, 'listar.html', {'usuarios': usuarios ,'llamarMensaje': llamarMensaje ,'mensaje': mensaje} )

#Edicion usuarios
@permission_required("usuarios.Administrador" , login_url="/")
def editar_usuario(request, username=None):
    try:
        usuario = Usuario.objects.get(cedula_usuario=username)
    except Usuario.DoesNotExist:
        llamarMensaje ="fracaso_usuario"
        mensaje = "El usuario "+str(username)+" No existe en el sistema"
        request.session["llamarMensaje"] = llamarMensaje
        request.session["mensaje"] = mensaje
        return redirect("listar_usuario")

    if request.method == 'POST':
        form = FormularioEditarUsuario(request.POST)
        #Si el formulario es valido y tiene datos
        if form.is_valid():

            #Capture la cedula del usuario
            usuario.first_name = form.cleaned_data["nombre_usuario"]
            usuario.last_name = form.cleaned_data["apellido_usuario"]
            usuario.email = form.cleaned_data["email"]
            usuario.is_active = form.cleaned_data["esta_activo"]

             #Actualiza  el usuario en la BD si hay excepcion
            try:
                usuario.save()
            except Exception as e:
                print(e)

            print("Voy a actualizar votante")

             # Si es votante, mostrar los campos facultad y codigo estudiante
            if form.cleaned_data["rol"] == "Votante":
                votante = Votante.objects.get(usuario__cedula_usuario=usuario.cedula_usuario)
                votante.codigo = form.cleaned_data["codigo_estudiante"]
                votante.plan = form.cleaned_data["plan_estudiante"]

                #Actualiza el votante en la BD
                try:
                    votante.save()
                except Exception as e:
                    print(e)

            #redireccionando a la vista
            llamarMensaje = "edito_usuario"
            mensaje = "Se editó el usuario " +  str(usuario.cedula_usuario) +" sactisfactoriamente"
            request.session['llamarMensaje'] = llamarMensaje
            request.session['mensaje'] = mensaje
            return redirect("listar_usuario")
    else:
        es_votante = False
        if username is None:
            return render(request, 'administrador.html')
        else:
            form = FormularioEditarUsuario()
            permissions = Permission.objects.filter(user=usuario)
            votante = Votante()
            if usuario.has_perm('usuarios.Votante'):
                print("entro a revisar votante")
                try:
                    votante = Votante.objects.get(usuario__cedula_usuario=usuario.cedula_usuario)
                    es_votante = True
                    form.initial = {'cedula_usuario': usuario.cedula_usuario, 'nombre_usuario': usuario.first_name, 'apellido_usuario': usuario.last_name,
                            'rol': permissions[0].codename, 'codigo_estudiante': votante.codigo, 'plan_estudiante': votante.plan, 'email': usuario.email, 'esta_activo': usuario.is_active}
                except Votante.DoesNotExist:
                    votante = None
            else:
                form.initial = {'cedula_usuario': usuario.cedula_usuario, 'nombre_usuario': usuario.first_name, 'apellido_usuario': usuario.last_name,
                            'rol': permissions[0].codename, 'email': usuario.email, 'esta_activo': usuario.is_active}

        return render(request, 'editar_usuario.html', {'form': form , 'votante': es_votante})

@permission_required("usuarios.Administrador", login_url="/")
def eliminar_usuario(request, username=None):
    if request.method == 'POST':

        usuario=Usuario.objects.get(cedula_usuario=username)

        # Si el usuario es votante
        if usuario.has_perm("usuarios.Votante"):
            votante = Votante.objects.get(usuario__cedula_usuario=usuario.cedula_usuario)

            try:
                votante.delete()
            except Exception as e:
                print(e)
        try:
            usuario.delete()
        except Exception as e:
            print(e)

        #redireccionando a la vista
        llamarMensaje = "elimino_usuario"
        mensaje = "Se eliminó el usuario " +  str(username) +" sactisfactoriamente"
        request.session['llamarMensaje'] = llamarMensaje
        request.session['mensaje'] = mensaje
        return redirect("listar_usuario")
