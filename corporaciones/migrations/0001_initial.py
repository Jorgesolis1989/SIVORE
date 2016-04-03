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
                ('facultad', models.OneToOneField(blank=True, null=True, to='corporaciones.Corporacion')),
            ],
            options={
                'ordering': ['name_corporation'],
                'db_table': 'corporacion',
            },
        ),
    ]
