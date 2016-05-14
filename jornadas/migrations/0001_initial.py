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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombrejornada', models.CharField(max_length=255)),
                ('fecha_inicio_jornada', models.DateTimeField()),
                ('fecha_final_jornada', models.DateTimeField()),
                ('is_active', models.BooleanField(default=True)),
                ('corporaciones', models.ManyToManyField(to='corporaciones.Corporacion')),
            ],
            options={
                'db_table': 'jornadas',
                'ordering': ['nombrejornada'],
            },
        ),
        migrations.CreateModel(
            name='Jornada_Corporacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('cantidad_planchas', models.IntegerField(default=0)),
                ('corporacion', models.ForeignKey(to='corporaciones.Corporacion')),
                ('jornada', models.ForeignKey(to='jornadas.Jornada')),
            ],
            options={
                'db_table': 'jornada_corporacion',
                'ordering': ['jornada'],
            },
        ),
    ]
