from django.conf.urls import patterns, url
from jornadas import views
urlpatterns = patterns('',
                       url(r'^crear/$', views.registro_jornada, name='registro_jornada'),
                       #url(r'^editar/(?P<idcorporacion>\w{1,50})/(?P<numplancha>\w{1,50})/$', views.editar_plancha, name='editar_plancha'),
                       #url(r'^listar/$', views.listar_planchas, name='listar_planchas'),
                       #url(r'^eliminar/(?P<idcorporacion>\w{1,50})/(?P<numplancha>\w{1,50})/$', views.eliminar_plancha, name='eliminar_plancha'),
                       )