from django.conf.urls import patterns, url
from candidatos import views
urlpatterns = patterns('',
                       url(r'^crear/$', views.registro_candidato, name='registro_candidato'),
                       #url(r'^editar/(?P<username>\w{1,50})$', views.editar_usuario, name='editar_usuario'),
                       #url(r'^listar/$', views.listar_usuario, name='listar_usuario'),
                       #url(r'^eliminar/(?P<username>\d*$)', views.eliminar_usuario, name='eliminar_usuario'),
                       )