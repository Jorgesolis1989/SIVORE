# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Corporacion',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('id_corporation', models.IntegerField()),
                ('name_corporation', models.CharField(max_length=45)),
                ('is_active', models.BooleanField(default=True)),
                ('facultad', models.ForeignKey(blank=True, to='corporaciones.Corporacion', null=True)),
            ],
            options={
                'ordering': ['name_corporation'],
                'db_table': 'corporacion',
            },
        ),
        migrations.CreateModel(
            name='Sede',
            fields=[
                ('codigo', models.IntegerField(serialize=False, primary_key=True)),
                ('nombre_sede', models.CharField(max_length=45)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='corporacion',
            name='sede',
            field=models.ForeignKey(to='corporaciones.Sede'),
        ),
    ]
