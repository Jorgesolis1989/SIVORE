# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('corporaciones', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='corporacion',
            name='facultad',
            field=models.ForeignKey(blank=True, to='corporaciones.Corporacion', null=True),
        ),
    ]
