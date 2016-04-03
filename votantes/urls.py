from django.conf.urls import patterns, url
from votantes import views

urlpatterns = patterns('',
                       url(r'^listar/$', views.listar_votantes, name='listar_votantes'),
                       )
