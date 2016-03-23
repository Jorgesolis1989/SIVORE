# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_auto_20160323_1752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='cedula_usuario',
            field=models.BigIntegerField(unique=True, primary_key=True, serialize=False),
        ),
    ]
