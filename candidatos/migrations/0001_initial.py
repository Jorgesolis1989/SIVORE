# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jornadas', '0001_initial'),
        ('votantes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Candidato',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('foto', models.ImageField(upload_to='candidatos')),
                ('tipo_candidato', models.CharField(max_length=45, blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('jornada_corporacion', models.ForeignKey(to='jornadas.Jornada_Corporacion')),
                ('votante', models.OneToOneField(to='votantes.Votante')),
            ],
            options={
                'ordering': ['votante__codigo'],
                'db_table': 'candidatos',
            },
        ),
    ]
