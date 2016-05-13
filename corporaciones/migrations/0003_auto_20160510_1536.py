# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('corporaciones', '0002_auto_20160510_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='corporacion',
            name='sede',
            field=models.ForeignKey(null=True, blank=True, to='corporaciones.Sede'),
        ),
    ]
