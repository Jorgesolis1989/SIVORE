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
                ('id_corporation', models.IntegerField(serialize=False, primary_key=True)),
                ('name_corporation', models.CharField(max_length=45)),
                ('is_active', models.BooleanField(default=True)),
                ('facultad', models.ForeignKey(blank=True, null=True, to='corporaciones.Corporacion')),
            ],
            options={
                'ordering': ['name_corporation'],
                'db_table': 'corporacion',
            },
        ),
    ]
