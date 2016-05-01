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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombrejornada', models.CharField(max_length=255)),
                ('fecha_inicio_jornada', models.DateTimeField()),
                ('fecha_final_jornada', models.DateTimeField()),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'jornadas',
                'ordering': ['nombrejornada'],
            },
        ),
        migrations.CreateModel(
            name='Jornada_Corporacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('corporacion', models.ForeignKey(to='corporaciones.Corporacion')),
                ('jornada', models.ForeignKey(to='jornadas.Jornada')),
            ],
            options={
                'db_table': 'jornada_corporacion',
                'ordering': ['jornada'],
            },
        ),
    ]
