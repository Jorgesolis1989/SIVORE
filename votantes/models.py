from django.db import models
from usuarios.models import Usuario
from corporaciones.models import Corporacion

class Votante(models.Model):
	usuario = models.ForeignKey(Usuario)
	codigo = models.BigIntegerField()
	plan = models.ForeignKey(Corporacion)

	class Meta:
		ordering = ["codigo"]
		db_table = 'votantes'

	def __str__(self):
		return '%s - %s  - %s - %s ' %(self.codigo , self.usuario.cedula_usuario, self.usuario.first_name, self.usuario.last_name)
