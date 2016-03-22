from django.db import models

class Corporacion(models.Model):
    id_corporation = models.IntegerField(unique=True, null=False, primary_key=True)
    name_corporation = models.CharField(max_length=45, null=False)
    id_facultad = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ["name_corporation"]
        db_table = 'corporacion'

        def __str__(self):
            return '%s - %s  - %s' % (self.id_corporation,   self.name_corporation, self.id_facultad)
