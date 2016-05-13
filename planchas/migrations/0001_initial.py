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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('numeroplancha', models.IntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('url_propuesta', models.URLField(blank=True, null=True)),
                ('num_votos', models.IntegerField(default=0, null=True)),
                ('candidato_principal', models.ForeignKey(related_name='principal', null=True, to='candidatos.Candidato')),
                ('candidato_suplente', models.ForeignKey(null=True, blank=True, default=None, to='candidatos.Candidato')),
                ('jornada_corporacion', models.ForeignKey(to='jornadas.Jornada_Corporacion')),
            ],
            options={
                'ordering': ['numeroplancha'],
                'db_table': 'planchas',
            },
        ),
    ]
