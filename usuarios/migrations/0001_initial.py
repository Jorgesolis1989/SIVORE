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
                ('user_ptr', models.OneToOneField(parent_link=True, to=settings.AUTH_USER_MODEL, auto_created=True)),
                ('cedula_usuario', models.BigIntegerField(unique=True, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name_plural': 'Usuarios_Sivore',
                'permissions': (('Administrador', 'Permisos de Administrador'), ('Superior', 'Permisos de Superior'), ('Votante', 'Permisos de Votante'), ('Candidato', 'Permisos de Candidato')),
                'ordering': ['first_name'],
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
