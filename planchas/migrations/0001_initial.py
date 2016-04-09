# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('corporaciones', '__first__'),
        ('candidatos', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plancha',
            fields=[
                ('numeroplancha', models.IntegerField(unique=True, serialize=False, primary_key=True)),
                ('candidato_principal', models.ForeignKey(to='candidatos.Candidato', related_name='principal')),
                ('candidato_suplente', models.ForeignKey(to='candidatos.Candidato', related_name='suplente')),
                ('corporacion', models.ForeignKey(to='corporaciones.Corporacion')),
            ],
            options={
                'db_table': 'planchas',
                'ordering': ['numeroplancha'],
            },
        ),
    ]
