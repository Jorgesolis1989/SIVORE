# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('corporaciones', '0002_corporacion_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jornada',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('nombrejornada', models.CharField(max_length=255)),
                ('fecha_jornada', models.CharField(max_length=255)),
                ('hora_inicio', models.DateField()),
                ('hora_final', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
                ('corporaciones', models.ForeignKey(to='corporaciones.Corporacion')),
            ],
            options={
                'db_table': 'jornadas',
                'ordering': ['nombrejornada'],
            },
        ),
    ]
