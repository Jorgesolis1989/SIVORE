# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('candidatos', '0002_candidato_votante'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidato',
            name='foto',
            field=models.ImageField(upload_to='candidatos'),
        ),
    ]
