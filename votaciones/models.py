from django.db import models
from usuarios.models import  Usuario
from jornadas.models import Jornada_Corporacion


class Votacion_Log(models.Model):
    jornada_corporacion = models.ForeignKey(Jornada_Corporacion)
    usuario = models.ForeignKey(Usuario)
    fecha_votacion = models.DateTimeField(auto_now_add=True, blank=True)
    is_active = models.BooleanField(default=True)


    class Meta:
        ordering = ["fecha_votacion"]
        db_table = 'votacion_log'

    def __str__(self):
        return 'Usuario %s Votó  por %s a %s ' % (self.usuario.cedula_usuario, self.jornada_corporacion.corporacion.name_corporation,
        self.fecha_votacion)