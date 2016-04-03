# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('candidatos', '0001_initial'),
        ('votantes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidato',
            name='votante',
            field=models.OneToOneField(to='votantes.Votante'),
        ),
    ]
