# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('corporaciones', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jornada',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('nombrejornada', models.CharField(max_length=255)),
                ('fecha_inicio_jornada', models.DateTimeField()),
                ('fecha_final_jornada', models.DateTimeField()),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['nombrejornada'],
                'db_table': 'jornadas',
            },
        ),
        migrations.CreateModel(
            name='Jornada_Corporacion',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('corporacion', models.ForeignKey(to='corporaciones.Corporacion')),
                ('jornada', models.ForeignKey(to='jornadas.Jornada')),
            ],
            options={
                'ordering': ['jornada'],
                'db_table': 'jornada_corporacion',
            },
        ),
    ]
