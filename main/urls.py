from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^accounts/login/$', views.LoginHandler.as_view(), name='LoginHandler'),
    url(r'^accounts/logout/$', views.logout_handler, name='logout_handler'),
    url(r'^analitycs/$', views.analitycs, name='analitycs'),
    url(r'^ss/$', views.ss, name='ss'),
]
