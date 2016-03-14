# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usuario',
            options={'permissions': (('Administrador', 'Administrador'), ('Superior', 'Superior'), ('Votante', 'Votante'), ('Candidato', 'Permisos de Candidato')), 'ordering': ['first_name'], 'verbose_name_plural': 'Usuarios_Sivore'},
        ),
    ]
