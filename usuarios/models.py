from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class PERSONA(models.Model):
	id = models.AutoField(primary_key=True)
	cedula = models.IntegerField(null= False,unique=True)
	nombre = models.CharField(max_length=30)
	apellidos = models.CharField(max_length=30)
	correo = models.EmailField(blank=True, verbose_name='e­mail')

	class Meta:
		ordering = ["nombre"]
		verbose_name_plural = "Personas"

	def __str__(self):
		return '%s %s' % (self.nombre, self.apellidos)

	class Admin:
		pass

class ROL(models.Model):
	nombre= models.CharField(max_length=40)

	class Meta:
		ordering = ["nombre"]
		verbose_name_plural = "Roles"

	def __str__(self):
		return self.nombre


class USUARIO(User):
	persona = models.ForeignKey(PERSONA, on_delete=models.CASCADE)
	rol = models.ForeignKey(ROL, on_delete=models.CASCADE)
	fecha_creacion = models.DateTimeField(auto_now=True)
	ultimo_acceso = models.DateTimeField(auto_now=True)
	observacion=models.CharField(max_length=30)

	class Meta:
		ordering = ["persona"]
		verbose_name_plural = "Usuarios"

	def __str__(self):
		return '%s - %s  - %s' % (self.persona.cedula,   self.persona.nombre , self.persona.apellidos)

	#added = models.DateTimeField(auto_now_add=True ,  default=timezone.now)
	#updated = models.DateTimeField(auto_now=True , default=timezone.now )