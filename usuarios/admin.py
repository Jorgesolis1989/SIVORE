from django.contrib import admin
from usuarios.models import USUARIO, PERSONA, ROL

# Register your models here.
admin.site.register(USUARIO)
admin.site.register(PERSONA)
admin.site.register(ROL)