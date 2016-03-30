from django.db import models

class Corporacion(models.Model):
    id_corporation = models.IntegerField(primary_key=True)
    name_corporation = models.CharField(max_length=45, null=False)
    facultad = models.ForeignKey('self', null=True, blank=True, unique=False)

    class Meta:
        ordering = ["name_corporation"]
        db_table = 'corporacion'


    def __str__(self):
        return '%s - %s ' % (self.id_corporation,   self.name_corporation)
