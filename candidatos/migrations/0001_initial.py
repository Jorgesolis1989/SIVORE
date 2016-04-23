# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jornadas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Candidato',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('foto', models.ImageField(upload_to='candidatos')),
                ('tipo_candidato', models.CharField(blank=True, max_length=45)),
                ('is_active', models.BooleanField(default=True)),
                ('jornada_corporacion', models.ForeignKey(to='jornadas.Jornada_Corporacion')),
            ],
            options={
                'db_table': 'candidatos',
                'ordering': ['votante__codigo'],
            },
        ),
    ]
