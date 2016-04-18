from django.db import models
from candidatos.models import Candidato
from corporaciones.models import Corporacion

class Jornada(models.Model):
    nombrejornada = models.CharField(null=False, max_length=255)
    fecha_inicio_jornada = models.DateTimeField()
    fecha_final_jornada = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["nombrejornada"]
        db_table = 'jornadas'

    def __str__(self):
        return '%s - %s   - %s  to  %s' % (self.nombrejornada, self.fecha_inicio_jornada.day,
                                           self.fecha_inicio_jornada.hour , self.fecha_final_jornada.hour )

class Jornada_Corporacion(models.Model):
    jornada = models.ForeignKey(Jornada, null=False)
    corporacion = models.ForeignKey(Corporacion, null=False)

    class Meta:
        ordering = ["jornada"]
        db_table = 'jornada_corporacion'

    def __str__(self):
        return '%s - %s' % (self.jornada.nombrejornada, self.corporacion.name_corporation )
