from django.conf.urls import patterns, url
from votaciones import views

urlpatterns = patterns('',
                       url(r'^tarjeton/$', views.mostrar_tarjeton, name='mostrar_tarjeton'),
                       url(r'^corporaciones/$', views.mostrar_corporaciones, name='mostrar_corporaciones'))
