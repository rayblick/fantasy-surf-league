from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<eventid>[0-9]+)/$', views.championshiptour, name='championshiptour'),
]
