from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import logout
from usuarios import views
import os


urlpatterns = [
	url(r'^admin/', include(admin.site.urls)),
	url(r'^$', views.login_view, name="login"),
	url(r'^administrador/', views.administrador_home , {'next_page': 'administrador.html'}, name="administrador_home"),
	url(r'^votante/', views.votante_home,   {'next_page': 'votante.html'}, name='votante_home'),
	url(r'^superior/$', views.superior_home,  {'next_page': 'superior.html'}, name='superior_home'),
	url(r'^logout', logout,  {'next_page': '/'} , name='logout'),
	url(r'^usuarios/', include('usuarios.urls')),
	url(r'^corporaciones/', include('corporaciones.urls')),
	url(r'^candidatos/', include('candidatos.urls')),
	url(r'^votantes/', include('votantes.urls')),
	url(r'^planchas/', include('planchas.urls')),
	url(r'^jornadas/', include('jornadas.urls')),
	url(r'^votaciones/', include('votaciones.urls')),
	url(r'^SIVORE/media/(.*)$', 'django.views.static.serve', {'document_root' : os.path.join(os.path.dirname(__file__), 'media')}),
]
