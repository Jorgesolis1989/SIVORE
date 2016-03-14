# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_auto_20160313_1658'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usuario',
            options={'verbose_name_plural': 'Usuarios_Sivore', 'permissions': (('Administrador', 'Permisos de Administrador'), ('Superior', 'Permisos de Superior'), ('Votante', 'Permisos de Votante'), ('Candidato', 'Permisos de Candidato')), 'ordering': ['first_name']},
        ),
    ]
