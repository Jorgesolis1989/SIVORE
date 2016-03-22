from django.db import models
from django.contrib.auth.models import User

class Usuario(User):
	cedula_usuario = models.IntegerField(null=False, unique=True, primary_key=True)

	class Meta:
		ordering = ["first_name"]
		verbose_name_plural = "Usuarios_Sivore"
		permissions = (("Administrador" , "Permisos de Administrador"),
					   ("Superior" , "Permisos de Superior"),
					   ("Votante" , "Permisos de Votante"),
					   ("Candidato" , "Permisos de Candidato"),)

		def __str__(self):
			return '%s - %s  - %s' % (self.cedula_usuario,   self.first_name, self.last_name	)

	#added = models.DateTimeField(auto_now_add=True ,  default=timezone.now)
	#updated = models.DateTimeField(auto_now=True , default=timezone.now )