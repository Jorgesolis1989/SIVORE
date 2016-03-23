# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='cedula_usuario',
            field=models.BigIntegerField(max_length=20, unique=True, primary_key=True, serialize=False),
        ),
    ]
