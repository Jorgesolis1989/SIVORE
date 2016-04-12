from django.conf.urls import patterns, url
from planchas import views
urlpatterns = patterns('',
                       url(r'^crear/$', views.registro_plancha, name='registro_plancha'),
                       url(r'^editar/(?P<idcorporacion>\w{1,50})/(?P<numplancha>\w{1,50})/$', views.editar_plancha, name='editar_plancha'),
                       url(r'^listar/$', views.listar_planchas, name='listar_planchas'),
                       )