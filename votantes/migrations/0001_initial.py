# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('corporaciones', '0001_initial'),
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Votante',
            fields=[
                ('codigo', models.BigIntegerField(primary_key=True, unique=True, serialize=False)),
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
