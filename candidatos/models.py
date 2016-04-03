from django.db import models
from votantes.models import Votante
from corporaciones.models import Corporacion

class Candidato(models.Model):
    votante = models.OneToOneField(Votante, null=False)
    foto = models.ImageField(upload_to='candidatos')
    tipo_candidato = models.CharField(max_length=45, blank=True, null=False)
    corporacion = models.ForeignKey(Corporacion, null=False)

    class Meta:
        ordering = ["votante__codigo"]
        db_table = 'candidatos'

    def __str__(self):
        return '%s - %s  %s - %s' % (self.votante.codigo, self.votante.usuario.first_name ,self.votante.usuario.last_name ,self.tipo_candidato)