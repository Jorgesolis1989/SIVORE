# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('corporaciones', '0001_initial'),
        ('votantes', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Candidato',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('foto', models.ImageField(upload_to='candidatos')),
                ('tipo_candidato', models.CharField(blank=True, max_length=45)),
                ('corporacion', models.ForeignKey(to='corporaciones.Corporacion')),
                ('votante', models.OneToOneField(to='votantes.Votante')),
            ],
            options={
                'ordering': ['votante__codigo'],
                'db_table': 'candidatos',
            },
        ),
    ]
