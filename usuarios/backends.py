# Clase para conectar el backend de la clase USUARIO y el user de Django.
from django.contrib.auth.models import User, check_password
from usuarios.models import USUARIO

class BackendUsuarios(object):
	def authenticate(self, username=None, password=None):
		try:
			usuario = USUARIO.objects.filter(persona__cedula=username)
			return usuario
			login_valid = usuario is not None
			if login_valid:
				pwd_valid = check_password(password, usuario.password)
				if pwd_valid:
					try:
						user = User.objects.filter(username=username)
					except User.DoesNotExist:
						user = User(username=usuario.persona.cedula, password=usuario.pasword)
						user.first_name = usuario.persona.nombre
						user.last_name = usuario.persona.apellidos
						user.last_login = usuario.ultimo_acceso
						user.permissions.add(usuario.rol.nombre)
						user.is_active = True
						user.save()
				return user
			return None
		except User.DoesNotExist:
			return None

	def get_user(self, user_id):
		try:
			return User.objects.get(username=user_id)
		except User.DoesNotExist:
			return None