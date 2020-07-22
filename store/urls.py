from django.conf.urls import url

from . import views # import views so we can use them in urls.


urlpatterns = [
    url(r'^$', views.listing, name='listing'),
    url(r'^profile/(?P<author_id>[0-9]+)/$', views.profile, name='profile'),
    url(r'^book/(?P<book_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^search/$', views.search, name='search'),
]