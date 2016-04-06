from django.conf.urls import patterns, url
from candidatos import views
urlpatterns = patterns('',
                       url(r'^crear/$', views.registro_candidato, name='registro_candidato'),
                       url(r'^editar/(?P<codigo>\w{1,50})$', views.editar_candidato, name='editar_candidato'),
                       url(r'^listar/$', views.listar_candidatos, name='listar_candidatos'),
                       #url(r'^eliminar/(?P<username>\d*$)', views.eliminar_usuario, name='eliminar_usuario'),
                       )