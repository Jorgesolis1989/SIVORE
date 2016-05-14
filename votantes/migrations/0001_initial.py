# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
        ('corporaciones', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Votante',
            fields=[
                ('codigo', models.BigIntegerField(unique=True, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('plan', models.ForeignKey(to='corporaciones.Corporacion')),
                ('usuario', models.ForeignKey(to='usuarios.Usuario')),
            ],
            options={
                'db_table': 'votantes',
                'ordering': ['codigo'],
            },
        ),
    ]
