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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('numeroplancha', models.IntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('url_propuesta', models.URLField(null=True, blank=True)),
                ('num_votos', models.IntegerField(null=True)),
                ('candidato_principal', models.ForeignKey(null=True, related_name='principal', to='candidatos.Candidato')),
                ('candidato_suplente', models.ForeignKey(default=None, blank=True, null=True, to='candidatos.Candidato')),
                ('jornada_corporacion', models.ForeignKey(to='jornadas.Jornada_Corporacion')),
            ],
            options={
                'db_table': 'planchas',
                'ordering': ['numeroplancha'],
            },
        ),
    ]
