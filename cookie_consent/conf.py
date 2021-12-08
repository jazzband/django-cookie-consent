# -*- coding: utf-8 -*-
from django.conf import settings  # NOQA

from appconf import AppConf


class CookieConsentConf(AppConf):
    NAME = b"cookie_consent"
    MAX_AGE = 60 * 60 * 24 * 365 * 1  # 1 year
    DECLINE = "-1"

    ENABLED = True

    OPT_OUT = False

    CACHE_BACKEND = "default"

    LOG_ENABLED = True
