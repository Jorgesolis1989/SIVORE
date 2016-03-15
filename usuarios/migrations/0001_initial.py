# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, to=settings.AUTH_USER_MODEL, auto_created=True)),
                ('cedula_usuario', models.IntegerField(serialize=False, unique=True, primary_key=True)),
            ],
            options={
                'permissions': (('Administrador', 'Permisos de Administrador'), ('Superior', 'Permisos de Superior'), ('Votante', 'Permisos de Votante'), ('Candidato', 'Permisos de Candidato')),
                'ordering': ['first_name'],
                'verbose_name_plural': 'Usuarios_Sivore',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
