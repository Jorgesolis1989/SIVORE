# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('votantes', '__first__'),
        ('jornadas', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Candidato',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('foto', models.ImageField(upload_to='fotos_candidatos/')),
                ('tipo_candidato', models.CharField(max_length=45, blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('jornada_corporacion', models.ForeignKey(to='jornadas.Jornada_Corporacion')),
                ('votante', models.ForeignKey(to='votantes.Votante')),
            ],
            options={
                'ordering': ['votante__codigo'],
                'db_table': 'candidatos',
            },
        ),
    ]
