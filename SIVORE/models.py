# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Candidato(models.Model):
    id_candidato = models.IntegerField(blank=True, null=True)
    esta_activo = models.IntegerField(blank=True, null=True)
    foto = models.CharField(max_length=45, blank=True, null=True)
    tipo_candidato = models.CharField(max_length=45, blank=True, null=True)
    persona_candidato_cedula = models.IntegerField(blank=True, null=True)
    corporacion_candidato_id = models.IntegerField(blank=True, null=True)
    plancha_candidato_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'candidato'


class Corporacion(models.Model):
    id_corporacion = models.IntegerField(blank=True, null=True)
    nombre = models.CharField(max_length=45, blank=True, null=True)
    id_facultad = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'corporacion'


class CorporacionLog(models.Model):
    id_corporacion_log = models.IntegerField(blank=True, null=True)
    id_corporacion = models.IntegerField(blank=True, null=True)
    fecha_accion = models.DateField(blank=True, null=True)
    accion_corporacion = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'corporacion_log'


class JornadaElectoral(models.Model):
    id_jornada_electoral = models.IntegerField(blank=True, null=True)
    nombre_jornada = models.CharField(max_length=45, blank=True, null=True)
    fecha_hora_inicio = models.DateField(blank=True, null=True)
    fecha_hora_fin = models.DateField(blank=True, null=True)
    esta_activa = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'jornada_electoral'


class JornadaElectoralCorporacion(models.Model):
    id_corporacion = models.IntegerField(blank=True, null=True)
    id_jornada_electoral = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'jornada_electoral_corporacion'


class JornadaElectoralLog(models.Model):
    id_jornada_electoral_log = models.IntegerField(blank=True, null=True)
    id_jornada_electoral = models.IntegerField(blank=True, null=True)
    fecha_accion = models.DateField(blank=True, null=True)
    accion = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'jornada_electoral_log'


class Persona(models.Model):
    cedula_persona = models.IntegerField(blank=True, null=True)
    nombres = models.CharField(max_length=45, blank=True, null=True)
    apellidos = models.CharField(max_length=45, blank=True, null=True)
    correo = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'persona'


class Plancha(models.Model):
    id_plancha = models.IntegerField(blank=True, null=True)
    numero_plancha = models.IntegerField(blank=True, null=True)
    numero_votos = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plancha'


class Rol(models.Model):
    id_rol = models.IntegerField(blank=True, null=True)
    nombre_rol = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rol'


class RolHasUsuario(models.Model):
    rol_id_rol = models.IntegerField(blank=True, null=True)
    rol_usuario_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rol_has_usuario'


class Usuario(models.Model):
    id_usuario = models.IntegerField(blank=True, null=True)
    password = models.CharField(max_length=30, blank=True, null=True)
    esta_activo = models.IntegerField(blank=True, null=True)
    fecha_creacion = models.DateField(blank=True, null=True)
    ultimo_acceso = models.DateField(blank=True, null=True)
    observacion = models.CharField(max_length=45, blank=True, null=True)
    persona_cedula_persona = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuario'


class UsuarioLog(models.Model):
    id_usuario_log = models.IntegerField(blank=True, null=True)
    ip_pc = models.IntegerField(blank=True, null=True)
    fecha_accion = models.DateField(blank=True, null=True)
    accion = models.CharField(max_length=45, blank=True, null=True)
    observacion = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuario_log'


class Votante(models.Model):
    id_votante = models.IntegerField(blank=True, null=True)
    codigo_votante = models.IntegerField(blank=True, null=True)
    cedula_votante = models.IntegerField(blank=True, null=True)
    plan = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'votante'


class VotanteLog(models.Model):
    id_votante_log = models.IntegerField(blank=True, null=True)
    codigo_votante = models.IntegerField(blank=True, null=True)
    id_corporacion = models.IntegerField(blank=True, null=True)
    fecha_votacion = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'votante_log'
