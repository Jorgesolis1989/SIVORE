from django.db import models
from candidatos.models import Candidato
from corporaciones.models import Corporacion

class Jornada(models.Model):
    nombrejornada = models.CharField(null=False, max_length=255)
    fecha_jornada = models.CharField(null=False, max_length=255)
    hora_inicio = models.DateField()
    hora_final = models.DateField()
    is_active = models.BooleanField(default=True)
    corporaciones = models.ForeignKey(Corporacion, null=False)

    class Meta:
        ordering = ["nombrejornada"]
        db_table = 'jornadas'

    def __str__(self):
        return '%s - %s  %s - %s' % (self.nombrejornada, self.hora_inicio, self.hora_final,self.corporaciones )