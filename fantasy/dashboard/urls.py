from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    #url(r'^mens/(?P<eventid>[0-9]+)/$', views.menstour, name='menstour'),
    #url(r'^womens/(?P<eventid>[0-9]+)/$', views.womenstour, name='womenstour'),
    url(r'^mens/(?P<year>[0-9]+)/(?P<stopnumber>[0-9]+)/$', views.menstour, name='menstour'),
    url(r'^womens/(?P<year>[0-9]+)/(?P<stopnumber>[0-9]+)/$', views.womenstour, name='womenstour'),
]
