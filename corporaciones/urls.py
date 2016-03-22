from django.conf.urls import patterns, url
from corporaciones import views
urlpatterns = patterns('',
                       url(r'^crear/$', views.registro_corporacion, name='registro_corporacion'),
                       url(r'^listar/$', views.listar_corporacion, name='listar_corporacion'),
                       url(r'^editar/(?P<id_corporation>\w{1,50})$', views.editar_corporacion, name='editar_corporacion'),
                       url(r'^eliminar/(?P<id_corporation>\d*$)', views.eliminar_corporacion, name='eliminar_corporacion'),
                       )
