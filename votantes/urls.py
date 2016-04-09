from django.conf.urls import patterns, url
from votantes import views

urlpatterns = patterns('',
                       url(r'^crear/$', views.registro_votante, name='registro_votante'),
                       #url(r'^editar/(?P<username>\w{1,50})$', views.editar_votante, name='editar_votante'),
                       url(r'^listar/$', views.listar_votantes, name='listar_votantes'),
                       url(r'^eliminar/(?P<username>\d*$)', views.eliminar_votante, name='eliminar_votante'),
                       )
