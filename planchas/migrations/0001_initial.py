# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jornadas', '0001_initial'),
        ('candidatos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plancha',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('numeroplancha', models.IntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('candidato_principal', models.ForeignKey(null=True, to='candidatos.Candidato', related_name='principal')),
                ('candidato_suplente', models.ForeignKey(default=None, null=True, blank=True, to='candidatos.Candidato')),
                ('jornada_corporacion', models.ForeignKey(to='jornadas.Jornada_Corporacion')),
            ],
            options={
                'db_table': 'planchas',
                'ordering': ['numeroplancha'],
            },
        ),
    ]
