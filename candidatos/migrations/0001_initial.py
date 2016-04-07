# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('votantes', '0001_initial'),
        ('corporaciones', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Candidato',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('foto', models.ImageField(upload_to='candidatos')),
                ('tipo_candidato', models.CharField(max_length=45, blank=True)),
                ('corporacion', models.ForeignKey(to='corporaciones.Corporacion')),
                ('votante', models.OneToOneField(to='votantes.Votante')),
            ],
            options={
                'db_table': 'candidatos',
                'ordering': ['votante__codigo'],
            },
        ),
    ]
