# -*- coding: utf-8 -*-
from django.urls import path

from .views import (
    TestPageView,
)

urlpatterns = [
    path("", TestPageView.as_view(), name='test_page'),
]
