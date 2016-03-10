from django.conf.urls import patterns, url
from usuarios import views
urlpatterns = patterns('',
                       url(r'^crear/$', views.registro_usuario, name='registro_usuario'),
                       url(r'^editar/(?P<username>\w{1,50})$', views.editar_usuario, name='editar_usuario'),
                       url(r'^listar/$', views.listar_usuario, name='listar_usuario'),
                       )
