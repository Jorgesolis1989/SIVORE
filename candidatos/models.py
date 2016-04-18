from django.db import models
from votantes.models import Votante
from corporaciones.models import Corporacion
from jornadas.models import Jornada_Corporacion

class Candidato(models.Model):
    votante = models.OneToOneField(Votante, null=False)
    foto = models.ImageField(upload_to='candidatos')
    tipo_candidato = models.CharField(max_length=45, blank=True, null=False)
    jornada_corporacion = models.ForeignKey(Jornada_Corporacion, null=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["votante__codigo"]
        db_table = 'candidatos'

    def __str__(self):
        return '%s - %s  %s - %s' % (self.votante.codigo, self.votante.usuario.first_name ,self.votante.usuario.last_name ,self.tipo_candidato)