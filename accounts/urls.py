from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    url(r'^login/$', views.auth_login, name='login'),
    url(r'^logout/$',
        auth_views.logout,
        {'template_name': 'accounts/logout.html'},
        name='logout'),
]
