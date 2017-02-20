from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^knowledge-areas/$', views.KnowledgeAreaList.as_view()),
]
