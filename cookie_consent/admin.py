# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import (
    Cookie,
    CookieGroup,
    LogItem,
)


class LogItemAdmin(admin.ModelAdmin):
    list_display = ('action', 'cookiegroup', 'version', 'created')
    list_filter = ('action', 'cookiegroup')


admin.site.register(LogItem, LogItemAdmin)
admin.site.register(Cookie)
admin.site.register(CookieGroup)
