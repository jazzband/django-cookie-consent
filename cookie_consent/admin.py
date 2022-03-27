# -*- coding: utf-8 -*-
from django.contrib import admin
from .conf import settings
from .models import (
    Cookie,
    CookieGroup,
    LogItem,
    CookieType,
)


class CookieAdmin(admin.ModelAdmin):
    list_display = ('varname', 'name', 'cookiegroup', 'cookietype', 'path', 'domain',
                    'get_version')
    search_fields = ('name', 'domain', 'cookietype__name', 'cookiegroup__varname',
                     'cookiegroup__name')
    readonly_fields = ('varname',)
    list_filter = ('cookiegroup',)


class CookieGroupAdmin(admin.ModelAdmin):
    list_display = ('varname', 'name', 'is_required', 'is_deletable',
                    'get_version', 'updated')
    search_fields = ('varname', 'name',)
    list_filter = ('is_required', 'is_deletable',)


class LogItemAdmin(admin.ModelAdmin):
    list_display = ('action', 'cookiegroup', 'version', 'created')
    list_filter = ('action', 'cookiegroup')
    readonly_fields = ('action', 'cookiegroup', 'version', 'created')
    date_hierarchy = 'created'


class CookieTypeAdmin(admin.ModelAdmin):
    list_display = ('name',) 
    search_fields = ('name',)

admin.site.register(Cookie, CookieAdmin)
admin.site.register(CookieGroup, CookieGroupAdmin)
admin.site.register(CookieType, CookieTypeAdmin)
if settings.COOKIE_CONSENT_LOG_ENABLED:
    admin.site.register(LogItem, LogItemAdmin)
