from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response, redirect, render
from django.template.context import RequestContext
from django.db.models import Q
import csv
from io import StringIO
import json
from usuarios.models import Usuario
from votantes.models import Votante
from candidatos.models import Candidato
from corporaciones.models import Corporacion
from planchas.models import Plancha
from jornadas.models import Jornada , Jornada_Corporacion
from django.core.urlresolvers import reverse_lazy


from django.utils import timezone
from django.conf import settings
timezone.activate(settings.TIME_ZONE)

from usuarios.forms import FormularioLogin
from usuarios.forms import FormularioRegistroUsuario, FormularioEditarUsuario, FormularioCargar
from votaciones.views import mostrar_corporaciones

#Método auxiliar para encontrar la vista del usuario
def retornar_vista(request, usuario):
    if usuario.has_perm("usuarios.Administrador"):
        return administrador_home(request, usuario)
    elif usuario.has_perm("usuarios.Votante"):
        return votante_home(request, usuario)
    elif usuario.has_perm("usuarios.Superior"):
        return superior_home(request, usuario)
    else:
        return login_view(request)

# Pagina principal para usuario Administrador
@permission_required("usuarios.Administrador" , login_url="/")
def administrador_home(request , usuario):
    return render(request, 'administrador.html', {'usuario': usuario})

# Pagina del home  para usuario Votante
@permission_required("usuarios.Votante" , login_url="/")
def votante_home(request, usuario):

    # Obteniendo los votantes asociados al usuario "Puede tener dos carreras"
    votantes_asociados = Votante.objects.filter(usuario__cedula_usuario=request.user.username)

    # Jornadas de acceso a las cuales el tiene acceso el/los votantes asociado
    jornadas_acceso = []
    for votante in votantes_asociados:
        jornadas_acceso += Jornada_Corporacion.objects.filter(Q(jornada__is_active=True) &
                                                (Q(corporacion__id_corporation=votante.plan.id_corporation) |
                                                Q(corporacion__id_corporation=votante.plan.facultad.id_corporation)))

    # Ordenando la lista por fecha de inicio
    jornadas_acceso.sort(key=lambda Jornada_Corporacion: Jornada_Corporacion.jornada.fecha_inicio_jornada)


    # La fecha de inicio es mayor a la fecha actual y la fecha final es menor a la fecha final de la jornada
    for jornada_acceso in jornadas_acceso:
        if ( utc_to_local(timezone.now()) >= utc_to_local(jornada_acceso.jornada.fecha_inicio_jornada)
             and utc_to_local(timezone.now()) <= utc_to_local(jornada_acceso.jornada.fecha_final_jornada)):
            return  mostrar_corporaciones(request,usuario,votantes_asociados,jornada_acceso.jornada)


    form = FormularioLogin()

    if not jornadas_acceso:
        mensaje = "Usted no tiene jornadas electorales cerca"
    else:
        mensaje = "No puede acceder todavía al sistema, su acceso es el " +str(jornadas_acceso[0].jornada.fecha_inicio_jornada) +\
                  " para la jornada "+str(jornadas_acceso[0].jornada.nombrejornada)

    return render(request , 'login.html', {"form":form , "mensaje": mensaje  })

# Pagina del home  para usuario Superior
@permission_required("usuarios.Superior" , login_url="/")
def superior_home(request, usuario):
    return render(request , 'superior.html', {'usuario': usuario})

def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

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

            try:
                #Consultando el usuario en la base de datos.
                usuario = Usuario.objects.get(cedula_usuario=cedula_usuario)

            #Si el usuario no existe, lo crea
            except Usuario.DoesNotExist:
                # Creando el usuario
                usuario = Usuario()
                createuser(usuario, form)
                # Borrando los datos del formulario y enviando el mensaje de sactisfacion
                form = FormularioRegistroUsuario()
                mensaje = "El usuario se guardo correctamente, la contraseña se envío al correo " + usuario.email
                llamarMensaje = "exito_usuario"


            else:
                # Si el usuario esta en la BD y no esta activo

                if not usuario.is_active:
                    createuser(usuario, form)
                    mensaje = "El usuario se guardo correctamente, la contraseña se envío al correo " + usuario.email
                    llamarMensaje = "exito_usuario"

                # Si el usuario ya existe en la BD y esta activo
                else:
                    mensaje = "El usuario " + str(cedula_usuario)  + " ya esta registrado"
                    llamarMensaje = "fracaso_usuario"

            request.session['llamarMensaje'] = llamarMensaje
            request.session['mensaje'] = mensaje
            return redirect("listar_usuario")

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
            userexist=0;
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

            mensaje = "Se crearon exitosamente " + str(usercreate) + " y se activaron " + str(useredit) + " votantes en el sistemas"
            if userexist != 0:
                mensaje = mensaje + ", además estaba activos " + str(userexist) + " usuarios"

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
    usuarios = Usuario.objects.filter(is_active=True)
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
            return redirect("listar_votantes")
    else:
        es_votante = False
        if username is None:
            return render(request, 'administrador.html')
        else:
            form = FormularioEditarUsuario()
            permissions = Permission.objects.filter(user=usuario)
            votante = Votante()
            if usuario.has_perm('usuarios.Votante'):
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
        try:
            usuario=Usuario.objects.get(cedula_usuario=username)
            usuario.is_active = False
            usuario.save()

            # si hay votante desactivelo
            votante = Votante.objects.filter(usuario__cedula_usuario=username)


            if votante:
                votante[0].is_active = False
                votante[0].save()


                # if es candidato desactivelo
                candidato = Candidato.objects.filter(votante__usuario__cedula_usuario=username)

                if candidato:
                    candidato[0].is_active = False
                    candidato[0].save()


                    # if es candidato plancha
                    plancha = Plancha.objects.filter(Q(candidato_principal__votante__usuario__cedula_usuario=username) |
                                                     Q(candidato_suplente__votante__usuario__cedula_usuario=username))

                    if plancha:
                        plancha[0].is_active = False
                        plancha[0].save()

        except Exception:
            llamarMensaje = "fracaso_usuario"
            mensaje = "Hubo un error, no se eliminó el usuario " +  str(username)

        #redireccionando a la vista
        else:
            llamarMensaje = "elimino_usuario"
            mensaje = "Se eliminó el usuario " +  str(username) +" sactisfactoriamente"


        request.session['llamarMensaje'] = llamarMensaje
        request.session['mensaje'] = mensaje
        return redirect("listar_usuario")

# Método auxiliar para crear
def createuser(usuario, form):
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

