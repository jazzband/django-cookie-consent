# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views import (
    TestPageView,
)

urlpatterns = patterns(
    '',
    url(r'^$',
        TestPageView.as_view(),
        name='test_page'),
)
