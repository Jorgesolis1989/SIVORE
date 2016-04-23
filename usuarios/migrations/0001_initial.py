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
                ('user_ptr', models.OneToOneField(auto_created=True, parent_link=True, to=settings.AUTH_USER_MODEL)),
                ('cedula_usuario', models.BigIntegerField(primary_key=True, unique=True, serialize=False)),
            ],
            options={
                'ordering': ['first_name'],
                'permissions': (('Administrador', 'Permisos de Administrador'), ('Superior', 'Permisos de Superior'), ('Votante', 'Permisos de Votante'), ('Candidato', 'Permisos de Candidato')),
                'verbose_name_plural': 'Usuarios_Sivore',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
