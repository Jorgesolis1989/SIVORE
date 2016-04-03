# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidato',
            fields=[
                ('id_candidato', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('votante_candidato_id', models.IntegerField(blank=True)),
                ('foto', models.CharField(null=True, blank=True, max_length=45)),
                ('tipo_candidato', models.CharField(blank=True, max_length=45)),
                ('corporacion_candidato_id', models.IntegerField(blank=True)),
            ],
            options={
                'ordering': ['id_candidato'],
                'db_table': 'candidato',
            },
        ),
    ]
