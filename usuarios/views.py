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
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.core.mail import EmailMessage

from django.shortcuts import render
from usuarios.models import Usuario
from usuarios.forms import FormularioLogin
from usuarios.forms import FormularioRegistroUsuario
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
    if request.method == 'POST':
        form = FormularioRegistroUsuario(request.POST)

        #Si el formulario es valido y tiene datos, limpielo
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

                #usuario.user_permissions.add(form.cleaned_data["rol"])
                print(password)

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
            else:
                form = FormularioRegistroUsuario()
                mensaje = "El usuario " + str(cedula_usuario)  + " ya esta registrado"

            return render_to_response('registro_usuario.html', {'mensaje': mensaje, 'form': form}, context_instance=RequestContext(request))
        else:
            form = FormularioRegistroUsuario()
            data = {
                'form': form,
            }
            return render_to_response('registro_usuario.html', data, context_instance=RequestContext(request))
    else:
        form = FormularioRegistroUsuario()

    return render(request, 'registro_usuario.html',{'mensaje': mensaje, 'form': form})

# Vista para listar usuarios
@permission_required("usuarios.Administrador" , login_url="/")
def listar_usuario(request):
    usuarios = Usuario.objects.all()
    return render(request, 'listar.html', {'usuarios': usuarios})

#Edicion usuarios
@permission_required("usuarios.Administrador" , login_url="/")
def editar_usuario(request, username=None):
    print(username)
    if username is None:
        return render(request, 'administrador.html')
    else:
        usuario = Usuario.objects.get(username=username)
        form = FormularioRegistroUsuario()
        form.initial = {'cedula_usuario': usuario.cedula_usuario, 'nombre_usuario': usuario.first_name , 'apellido_usuario': usuario.last_name ,
                        'rol': "Administrador" , 'email': usuario.email }
    return render(request, 'editar_usuario.html', {'form': form})