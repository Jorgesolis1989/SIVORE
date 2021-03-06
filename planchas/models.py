from django.db import models
from candidatos.models import Candidato
from jornadas.models import Jornada_Corporacion

class Plancha(models.Model):
    numeroplancha = models.IntegerField(null=False, unique=False)
    jornada_corporacion = models.ForeignKey(Jornada_Corporacion, null=False)
    candidato_principal = models.ForeignKey(Candidato, null=True, related_name='principal')
    candidato_suplente = models.ForeignKey(Candidato, null=True, blank=True, unique=False, default=None)
    is_active = models.BooleanField(default=True)
    url_propuesta = models.URLField(null=True, blank=True)
    num_votos = models.IntegerField(null=True, default= 0)

    class Meta:
        ordering = ["numeroplancha"]
        db_table = 'planchas'

    def __str__(self):
        return '%s - %s  %s - %s - %s' % (self.numeroplancha, self.jornada_corporacion.corporacion, self.candidato_principal,
                                     self.candidato_suplente, self.url_propuesta)