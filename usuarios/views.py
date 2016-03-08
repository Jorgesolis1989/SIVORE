from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
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
from usuarios.models import USUARIO , PERSONA , ROL
from usuarios.forms import FormularioLogin
from usuarios.forms import FormularioRegistroUsuario


#Método auxiliar para encontrar la vista del usuario
def retornar_vista(request , usuario):
    if usuario.rol.nombre == "Administrador":
        return administrador_home(request, usuario)
    elif usuario.rol.nombre == "Votante":
        return votante_home(request, usuario)
    else:
        return superior_home(request, usuario)

# Pagina principal para usuario Administrador
@login_required()
def administrador_home(request , usuario):
    return render(request, 'administrador.html', {'usuario': usuario})


# Pagina del home  para usuario Votante
def votante_home(request, usuario):
    return render(request , 'votante.html', {'usuario': usuario})

# Pagina del home  para usuario Superior
def superior_home(request, usuario):
    return render(request ,  'superior.html', {'usuario': usuario})


#Pagina de login
def login_view(request):
    mensaje = ""
    if request.user.is_authenticated() and not request.user.is_superuser:
        usuario = USUARIO.objects.get(persona__cedula=request.user.username)
        return retornar_vista(request, usuario)

    elif request.method == 'POST':
        form = FormularioLogin(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            acceso = authenticate(username=cd['username'], password=cd['password'])
            if acceso is not None:
                if acceso.is_active:
                    login(request, acceso)
                    usuario = USUARIO.objects.get(persona__cedula=cd['username'])
                    #Redireccionar
                    return retornar_vista(request, usuario)
                else:
                   mensaje = "Usuario no activado"
            else:
                   mensaje = "Datos erróneos. Por favor, inténtelo otra vez.    "
    else:
        form = FormularioLogin()
    return render(request, 'login.html', {'mensaje': mensaje, 'form': form})

#Vista de registro de usuarios
def registro_usuario(request):
    mensaje = ""
    if request.method == 'POST':
        form = FormularioRegistroUsuario(request.POST)
        if form.is_valid():
            cedula_usuario = form.cleaned_data["cedula_usuario"]
            persona = PERSONA.objects.filter(cedula=cedula_usuario)
            print(persona)
            if not persona:
                nombre_usuario = form.cleaned_data["nombre_usuario"]
                apellido_usuario = form.cleaned_data["apellido_usuario"]
                correo = form.cleaned_data["email"]
                rol = form.cleaned_data["rol"]

                # Creando la persona.
                persona = PERSONA()
                persona.cedula = cedula_usuario
                persona.nombre = nombre_usuario
                persona.apellidos = apellido_usuario
                persona.correo = correo

                try:
                    persona.save()
                except Exception as e:
                    print(e)

                # Creando el usuario
                usuario = USUARIO()
                usuario.username = cedula_usuario
                usuario.persona = PERSONA.objects.get(cedula=cedula_usuario)
                usuario.rol = ROL.objects.get(nombre=rol)
                password = User.objects.make_random_password()
                print("El password es : "+password)
                usuario.set_password(password)
                usuario.observacion =  "Creando USUARIO " + str(cedula_usuario)

                send_mail('Envío de correo electronico', correo, 'sivoreunivalle@gmail.com', [correo], fail_silently=False)
                #email = EmailMessage('Envío de contrasena Acceso SIVORE', 'contrasena: '+password , to=[correo])
                #email.send()

                try:
                    usuario.save()
                except Exception as e:
                    print(e)

                # Enviando contraseña al correo electronico registrado.
                form = FormularioRegistroUsuario()
                mensaje = "El usuario se guardo correctamente, la contraseña se envío al correo " + correo
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

def listar_usuario(request):
    return render(request, 'listar.html')

