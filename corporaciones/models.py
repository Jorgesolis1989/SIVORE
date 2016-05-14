from django.db import models

class Sede(models.Model):
    codigo =  models.IntegerField(primary_key=True)
    nombre_sede = models.CharField(max_length=45, null=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '%s --  %s' % (self.codigo,   self.nombre_sede)


class Corporacion(models.Model):
    id_corporation = models.IntegerField(unique=False)
    name_corporation = models.CharField(max_length=45, null=False)
    facultad = models.ForeignKey('self', null=True, blank=True, unique=False)
    is_active = models.BooleanField(default=True)
    sede = models.ForeignKey(Sede , null=True, blank=True)
    class Meta:
        ordering = ["name_corporation"]
        db_table = 'corporacion'


    def __str__(self):
        if self.sede is None:
            return '%s - %s ' % (self.id_corporation,   self.name_corporation )
        else:
            return '%s - %s Sede %s' % (self.id_corporation,   self.name_corporation , self.sede.nombre_sede)

