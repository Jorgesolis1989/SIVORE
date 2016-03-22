from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Permission
from django.views.decorators.csrf import requires_csrf_token
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import permission_required
#from  usuarios.forms import FormularioLogin
from django.core.urlresolvers import reverse_lazy
import hashlib
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response , redirect
from django.template.context import RequestContext
from django.core.mail import EmailMessage

from django.shortcuts import render
from usuarios.models import Usuario
from usuarios.forms import FormularioLogin
from usuarios.forms import FormularioRegistroUsuario, FormularioEditarUsuario
from usuarios.backends import BackendUsuarios

#Método auxiliar para encontrar la vista del usuario
def retornar_vista(request , usuario):
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
@permission_required("usuarios.Administrador" , login_url="/")
def registro_usuario(request):
    mensaje = ""
    llamarMensaje = ""
    if request.method == 'POST':
        form = FormularioRegistroUsuario(request.POST)

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

                usuario.user_permissions.add(Permission.objects.get(codename=form.cleaned_data["rol"]))

                form = FormularioRegistroUsuario()
                mensaje = "El usuario se guardo correctamente, la contraseña se envío al correo " + usuario.email
                llamarMensaje = "exito_usuario"

            else:
                form = FormularioRegistroUsuario()
                mensaje = "El usuario " + str(cedula_usuario)  + " ya esta registrado"
                llamarMensaje = "fracaso_usuario"


            return render_to_response('registro_usuario.html', {'mensaje': mensaje, 'form': form , 'llamarMensaje': llamarMensaje}, context_instance=RequestContext(request))
        else:
            form = FormularioRegistroUsuario()
            data = {
                'form': form,
            }
            return render_to_response('registro_usuario.html', data, context_instance=RequestContext(request))
    else:
        form = FormularioRegistroUsuario()

    return render(request, 'registro_usuario.html',{'mensaje': mensaje, 'form': form })

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
    usuario = Usuario.objects.get(cedula_usuario=username)
    if request.method == 'POST':
        form = FormularioEditarUsuario(request.POST)
        #Si el formulario es valido y tiene datos
        if form.is_valid():
            #Capture la cedula del usuario
            usuario.first_name = form.cleaned_data["nombre_usuario"]
            usuario.last_name = form.cleaned_data["apellido_usuario"]
            usuario.email = form.cleaned_data["email"]
            usuario.is_active = form.cleaned_data["esta_activo"]
            permission =Permission.objects.get(codename=form.cleaned_data["rol"])
            usuario.user_permissions.clear()
            usuario.user_permissions.add(permission)

             #Actualiza  el usuario en la BD si hay excepcion
            try:
                usuario.save()
            except Exception as e:
                print(e)

            #redireccionando a la vista
            llamarMensaje = "edito_usuario"
            mensaje = "Se editó el usuario " +  str(usuario.cedula_usuario) +" sactisfactoriamente"
            request.session['llamarMensaje'] = llamarMensaje
            request.session['mensaje'] = mensaje
            return redirect("listar_usuario")
    else:
        if username is None:
            return render(request, 'administrador.html')
        else:
            form = FormularioEditarUsuario()
            permissions = Permission.objects.filter(user=usuario)

            form.initial = {'cedula_usuario': usuario.cedula_usuario, 'nombre_usuario': usuario.first_name , 'apellido_usuario': usuario.last_name ,
                            'rol': permissions[0].codename , 'email': usuario.email , 'esta_activo': usuario.is_active  }
        return render(request, 'editar_usuario.html', {'form': form})

@permission_required("usuarios.Administrador", login_url="/")
def eliminar_usuario(request, username=None):
    if request.method == 'POST':
        usuario=Usuario.objects.get(cedula_usuario=username)
        print('POST',"ENTRO AQUI")
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
