# coding=utf-8
"""FreeTimeLance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
import django.contrib.auth.views as auth_view

from project.views import CustomerSignUpView, CustomerAcceptInvite, show_404

urlpatterns = [
    url(r'^invitations/accept-invite/(?P<key>\w+)/?$',
        CustomerAcceptInvite.as_view(), name='accept-invite'),
    url(r'^invitations/', include('invitations.urls',
                                  namespace='invitations')),
    url(r'^admin/', admin.site.urls),
    url(r'', include('project.urls')),
    url('^accept-invite/register/$', show_404, name='account_signup'),
    url('^accept-invite/register/(?P<key>\w+)/?$',
        CustomerSignUpView.as_view(), name='account_signup'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^logout/$', auth_view.logout, {'next_page': '/'}),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),

    ]
