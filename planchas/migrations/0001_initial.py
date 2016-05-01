# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('candidatos', '0001_initial'),
        ('jornadas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plancha',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numeroplancha', models.IntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('url_propuesta', models.URLField(blank=True, null=True)),
                ('num_votos', models.IntegerField(null=True)),
                ('candidato_principal', models.ForeignKey(to='candidatos.Candidato', related_name='principal', null=True)),
                ('candidato_suplente', models.ForeignKey(to='candidatos.Candidato', blank=True, default=None, null=True)),
                ('jornada_corporacion', models.ForeignKey(to='jornadas.Jornada_Corporacion')),
            ],
            options={
                'db_table': 'planchas',
                'ordering': ['numeroplancha'],
            },
        ),
    ]
