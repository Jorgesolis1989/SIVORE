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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('numeroplancha', models.IntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('candidato_principal', models.ForeignKey(related_name='principal', to='candidatos.Candidato')),
                ('candidato_suplente', models.ForeignKey(default=None, null=True, to='candidatos.Candidato', blank=True)),
                ('jornada_corporacion', models.ForeignKey(to='jornadas.Jornada_Corporacion')),
            ],
            options={
                'db_table': 'planchas',
                'ordering': ['numeroplancha'],
            },
        ),
    ]
