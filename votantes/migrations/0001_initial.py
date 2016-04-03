# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
        ('corporaciones', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Votante',
            fields=[
                ('codigo', models.BigIntegerField(unique=True, primary_key=True, serialize=False)),
                ('plan', models.ForeignKey(to='corporaciones.Corporacion')),
                ('usuario', models.ForeignKey(to='usuarios.Usuario')),
            ],
            options={
                'ordering': ['codigo'],
                'db_table': 'votantes',
            },
        ),
    ]
