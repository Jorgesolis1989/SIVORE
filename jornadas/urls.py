from django.conf.urls import patterns, url
from jornadas import views
urlpatterns = patterns('',
                       url(r'^crear/$', views.registro_jornada, name='registro_jornada'),
                       url(r'^editar/(?P<id>\w{1,50})$', views.editar_jornada, name='editar_jornada'),
                       url(r'^listar/$', views.listar_jornadas, name='listar_jornadas'),
                       url(r'^eliminar/(?P<idjornada>\w{1,50})$', views.eliminar_jornada, name='eliminar_plancha'),
                       )