from django.db import models
from corporaciones.models import Corporacion

class Jornada(models.Model):
    nombrejornada = models.CharField(null=False, max_length=255)
    fecha_inicio_jornada = models.DateTimeField()
    fecha_final_jornada = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    corporaciones = models.ManyToManyField(Corporacion)

    class Meta:
        ordering = ["nombrejornada"]
        db_table = 'jornadas'

    def __str__(self):
        return '%s -   %s ' % (self.nombrejornada, self.fecha_inicio_jornada.date())

    def corporation_names(self):
        return ',  '.join([(a.name_corporation + (" "if a.sede is None else  " Sede "+ a.sede.nombre_sede )) for a in self.corporaciones.all()])
    corporation_names.short_description = "Corporacion Names"


class Jornada_Corporacion(models.Model):
    jornada = models.ForeignKey(Jornada, null=False)
    corporacion = models.ForeignKey(Corporacion, null=False)
    is_active = models.BooleanField(default=True)
    cantidad_planchas = models.IntegerField(default=0)

    class Meta:
        ordering = ["jornada"]
        db_table = 'jornada_corporacion'

    def __str__(self):
        return '%s - %s el %s' % ( self.corporacion , self.jornada.nombrejornada , self.jornada.fecha_inicio_jornada.date())