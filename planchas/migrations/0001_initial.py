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
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('numeroplancha', models.IntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('url_propuesta', models.URLField(blank=True, null=True)),
                ('num_votos', models.IntegerField(null=True, default=0)),
                ('candidato_principal', models.ForeignKey(null=True, to='candidatos.Candidato', related_name='principal')),
                ('candidato_suplente', models.ForeignKey(default=None, blank=True, null=True, to='candidatos.Candidato')),
                ('jornada_corporacion', models.ForeignKey(to='jornadas.Jornada_Corporacion')),
            ],
            options={
                'ordering': ['numeroplancha'],
                'db_table': 'planchas',
            },
        ),
    ]
