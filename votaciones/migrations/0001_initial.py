# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
        ('jornadas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Votacion_Log',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('fecha_votacion', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('jornada_corporacion', models.ForeignKey(to='jornadas.Jornada_Corporacion')),
                ('usuario', models.ForeignKey(to='usuarios.Usuario')),
            ],
            options={
                'db_table': 'votacion_log',
                'ordering': ['fecha_votacion'],
            },
        ),
    ]
