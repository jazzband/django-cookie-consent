# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from .views import (
    CookieGroupListView,
    CookieGroupAcceptView,
    CookieGroupDeclineView,
)

urlpatterns = [
    url(r'^accept/$',
        csrf_exempt(CookieGroupAcceptView.as_view()),
        name='cookie_consent_accept_all'),
    url(r'^accept/(?P<varname>.*)/$',
        csrf_exempt(CookieGroupAcceptView.as_view()),
        name='cookie_consent_accept'),
    url(r'^decline/(?P<varname>.*)/$',
        csrf_exempt(CookieGroupDeclineView.as_view()),
        name='cookie_consent_decline'),
    url(r'^decline/$',
        csrf_exempt(CookieGroupDeclineView.as_view()),
        name='cookie_consent_decline_all'),
    url(r'^$',
        CookieGroupListView.as_view(),
        name='cookie_consent_cookie_group_list'),
]
