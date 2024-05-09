# -*- coding: utf-8 -*-
from copy import deepcopy
from unittest import mock

from django.conf import settings
from django.core.cache import caches
from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings

from cookie_consent.cache import CACHE_KEY, delete_cache
from cookie_consent.models import Cookie, CookieGroup, validate_cookie_name

patch_caches = override_settings(
    COOKIE_CONSENT_CACHE_BACKEND="tests",
    CACHES={
        **deepcopy(settings.CACHES),
        "tests": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        },
    },
)


class CacheMixin:
    def populateCache(self):
        cache = caches["tests"]
        cache.set(CACHE_KEY, {}, timeout=3600)

    def assertCacheNotPopulated(self):
        cache = caches["tests"]
        has_key = cache.has_key(CACHE_KEY)
        self.assertFalse(has_key)


@patch_caches
class CookieGroupTest(CacheMixin, TestCase):
    def setUp(self):
        self.addCleanup(delete_cache)

        self.cookie_group = CookieGroup.objects.create(
            varname="optional",
            name="Optional",
        )
        self.cookie = Cookie.objects.create(
            cookiegroup=self.cookie_group,
            name="foo",
        )

    def test_get_version(self):
        self.assertEqual(
            self.cookie_group.get_version(), self.cookie.created.isoformat()
        )

    def test_bulk_delete(self):
        self.populateCache()

        deleted_objs_count, _ = CookieGroup.objects.filter(
            id=self.cookie_group.id
        ).delete()

        # Deleting a CookieGroup also deletes the associated Cookies, that's why we expect a count of 2.
        self.assertEqual(deleted_objs_count, 2)
        self.assertCacheNotPopulated()

    def test_bulk_update(self):
        self.populateCache()

        updated_objs_count = CookieGroup.objects.filter(id=self.cookie_group.id).update(
            name="Optional2"
        )

        self.assertEqual(updated_objs_count, 1)
        self.assertCacheNotPopulated()


@patch_caches
class CookieTest(CacheMixin, TestCase):
    def setUp(self):
        self.addCleanup(delete_cache)

        self.cookie_group = CookieGroup.objects.create(
            varname="optional",
            name="Optional",
        )
        self.cookie = Cookie.objects.create(
            cookiegroup=self.cookie_group,
            name="foo",
            domain=".example.com",
        )

    def test_varname(self):
        self.assertEqual(self.cookie.varname, "optional=foo:.example.com")

    def test_bulk_delete(self):
        self.populateCache()

        deleted_objs_count, _ = Cookie.objects.filter(id=self.cookie.id).delete()

        self.assertEqual(deleted_objs_count, 1)
        self.assertCacheNotPopulated()

    def test_bulk_update(self):
        self.populateCache()

        updated_objs_count = Cookie.objects.filter(id=self.cookie.id).update(
            name="foo2"
        )

        self.assertEqual(updated_objs_count, 1)
        self.assertCacheNotPopulated()


class ValidateCookieNameTest(TestCase):
    def test_valid(self):
        validate_cookie_name("_foo-bar")

    def test_invalid(self):
        invalid_names = (
            "space inside",
            "a!b",
            "$",
        )
        for name in invalid_names:
            with self.assertRaises(ValidationError):
                validate_cookie_name("no spaces")
