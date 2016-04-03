# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('corporaciones', '0001_initial'),
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Votante',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('codigo', models.BigIntegerField()),
                ('plan', models.ForeignKey(to='corporaciones.Corporacion')),
                ('usuario', models.ForeignKey(to='usuarios.Usuario')),
            ],
            options={
                'ordering': ['codigo'],
                'db_table': 'votantes',
            },
        ),
    ]
