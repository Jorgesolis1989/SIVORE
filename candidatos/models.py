from django.db import models

class Candidato(models.Model):
    id_candidato = models.IntegerField(unique=True, null=False, primary_key=True)
    votante_candidato_id = models.IntegerField(blank=True, null=False)
    foto = models.CharField(max_length=45, blank=True, null=True)
    tipo_candidato = models.CharField(max_length=45, blank=True, null=False)
    corporacion_candidato_id = models.IntegerField(blank=True, null=False)

    class Meta:
        ordering = ["id_candidato"]
        db_table = 'candidato'

        def __str__(self):
            return '%s - %s  - %s' % (self.id_candidato, self.tipo_candidato, self.votante_candidato_id)