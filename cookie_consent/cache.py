# -*- coding: utf-8 -*-
from django.core.cache import caches

from cookie_consent.conf import settings

CACHE_KEY = "cookie_consent_cache"
CACHE_TIMEOUT = 60 * 60


def _get_cache():
    """
    Lazily wrap around django.core.cache.

    This prevents the cache object to be resolved at import-time, which breaks the
    `django.test.override_settings` functionality for projects adding tests for this
    package, see https://github.com/bmihelac/django-cookie-consent/issues/41.
    """
    return caches[settings.COOKIE_CONSENT_CACHE_BACKEND]


def delete_cache():
    cache = _get_cache()
    cache.delete(CACHE_KEY)


def all_cookie_groups():
    cache = _get_cache()
    items = cache.get(CACHE_KEY)
    if items is None:
        from cookie_consent.models import CookieGroup

        qs = CookieGroup.objects.filter(is_required=False)
        qs = qs.prefetch_related("cookie_set")
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
