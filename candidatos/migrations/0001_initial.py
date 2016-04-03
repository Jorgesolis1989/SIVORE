# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('corporaciones', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Candidato',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('foto', models.ImageField(upload_to='media/')),
                ('tipo_candidato', models.CharField(blank=True, max_length=45)),
                ('corporacion', models.ForeignKey(to='corporaciones.Corporacion')),
            ],
            options={
                'ordering': ['votante__codigo'],
                'db_table': 'candidatos',
            },
        ),
    ]
