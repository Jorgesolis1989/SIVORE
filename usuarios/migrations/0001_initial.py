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
            name='PERSONA',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('cedula', models.IntegerField(unique=True)),
                ('nombre', models.CharField(max_length=30)),
                ('apellidos', models.CharField(max_length=30)),
                ('correo', models.EmailField(max_length=254, verbose_name='e\xadmail', blank=True)),
            ],
            options={
                'verbose_name_plural': 'Personas',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='ROL',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('nombre', models.CharField(max_length=40)),
            ],
            options={
                'verbose_name_plural': 'Roles',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='USUARIO',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, serialize=False, primary_key=True, to=settings.AUTH_USER_MODEL, auto_created=True)),
                ('fecha_creacion', models.DateTimeField(auto_now=True)),
                ('ultimo_acceso', models.DateTimeField(auto_now=True)),
                ('observacion', models.CharField(max_length=30)),
                ('persona', models.ForeignKey(to='usuarios.PERSONA')),
                ('rol', models.ForeignKey(to='usuarios.ROL')),
            ],
            options={
                'verbose_name_plural': 'Usuarios',
                'ordering': ['persona'],
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
