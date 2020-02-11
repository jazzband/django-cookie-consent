# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from .views import (
    TestPageView,
)

urlpatterns = [
    url(r'^$',
        TestPageView.as_view(),
        name='test_page'),
]
