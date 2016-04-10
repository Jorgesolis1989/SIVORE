from django.db import models
from usuarios.models import Usuario
from corporaciones.models import Corporacion

class Votante(models.Model):
	usuario = models.ForeignKey(Usuario)
	codigo = models.BigIntegerField(unique=True, primary_key=True)
	plan = models.ForeignKey(Corporacion)
	is_active = models.BooleanField(default=True)

	class Meta:
		ordering = ["codigo"]
		db_table = 'votantes'

	def __str__(self):
		return '%s - %s   %s - %s %s' %(self.codigo , self.usuario.first_name, self.usuario.last_name, self.plan.id_corporation, self.plan.name_corporation)
