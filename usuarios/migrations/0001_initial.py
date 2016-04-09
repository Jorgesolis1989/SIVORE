# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('user_ptr', models.OneToOneField(to=settings.AUTH_USER_MODEL, parent_link=True, auto_created=True)),
                ('cedula_usuario', models.BigIntegerField(serialize=False, primary_key=True, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Usuarios_Sivore',
                'ordering': ['first_name'],
                'permissions': (('Administrador', 'Permisos de Administrador'), ('Superior', 'Permisos de Superior'), ('Votante', 'Permisos de Votante'), ('Candidato', 'Permisos de Candidato')),
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
