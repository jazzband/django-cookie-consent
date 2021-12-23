# -*- coding: utf-8 -*-
from django.core.cache import caches
from cookie_consent.conf import settings


cache = caches[settings.COOKIE_CONSENT_CACHE_BACKEND]



CACHE_KEY = 'cookie_consent_cache'
CACHE_TIMEOUT = 60 * 60


def delete_cache():
    cache.delete(CACHE_KEY)


def all_cookie_groups():
    items = cache.get(CACHE_KEY)
    if items is None:
        from cookie_consent.models import CookieGroup
        qs = CookieGroup.objects.filter(is_required=False)
        qs = qs.prefetch_related('cookie_set')
        items = dict([(g.varname, g) for g in qs])
        cache.set(CACHE_KEY, items, CACHE_TIMEOUT)
    return items


def get_cookie_group(varname):
    return all_cookie_groups().get(varname)


def get_cookie(cookie_group, name, domain):
    for cookie in cookie_group.cookie_set.all():
        if cookie.name == name and cookie.domain == domain:
            return cookie
    return None
