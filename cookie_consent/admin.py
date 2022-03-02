# -*- coding: utf-8 -*-
from django.contrib import admin
from .conf import settings
from .models import (
    Cookie,
    CookieGroup,
    LogItem,
)


class CookieAdmin(admin.ModelAdmin):
    list_display = ('varname', 'name', 'cookiegroup', 'path', 'domain',
                    'get_version')
    search_fields = ('name', 'domain', 'cookiegroup__varname',
                     'cookiegroup__name')
    readonly_fields = ('varname',)
    list_filter = ('cookiegroup',)


class CookieGroupAdmin(admin.ModelAdmin):
    list_display = ('varname', 'name', 'is_required', 'is_deletable',
                    'get_version')
    search_fields = ('varname', 'name',)
    list_filter = ('is_required', 'is_deletable',)


class LogItemAdmin(admin.ModelAdmin):
    list_display = ('action', 'cookiegroup', 'version', 'created')
    list_filter = ('action', 'cookiegroup')
    readonly_fields = ('action', 'cookiegroup', 'version', 'created')
    date_hierarchy = 'created'


admin.site.register(Cookie, CookieAdmin)
admin.site.register(CookieGroup, CookieGroupAdmin)
if settings.COOKIE_CONSENT_LOG_ENABLED:
    admin.site.register(LogItem, LogItemAdmin)
