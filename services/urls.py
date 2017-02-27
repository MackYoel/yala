from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^knowledge-areas/$', views.KnowledgeAreaList.as_view()),
    url(r'^knowledge-areas/(?P<area_pk>[0-9]+)/themes/$', views.ThemeList.as_view()),

    url(r'^themes/(?P<theme_pk>[0-9]+)/issues/$', views.IssueList.as_view()),
    url(r'^themes/(?P<theme_pk>[0-9]+)/issues/(?P<pk>[0-9]+)/$', views.IssueDetail.as_view()),
]
