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
                ('id_corporation', models.IntegerField(primary_key=True, serialize=False)),
                ('name_corporation', models.CharField(max_length=45)),
                ('is_active', models.BooleanField(default=True)),
                ('facultad', models.ForeignKey(to='corporaciones.Corporacion', blank=True, null=True)),
            ],
            options={
                'db_table': 'corporacion',
                'ordering': ['name_corporation'],
            },
        ),
    ]
