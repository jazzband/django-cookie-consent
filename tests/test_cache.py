# -*- coding: utf-8 -*-
from django.test import TestCase, override_settings

from cookie_consent.cache import get_cookie, get_cookie_group
from cookie_consent.models import Cookie, CookieGroup


class CacheTest(TestCase):
    def setUp(self):
        self.cookie_group = CookieGroup.objects.create(
            varname="optional",
            name="Optional",
        )
        self.cookie = Cookie.objects.create(
            cookiegroup=self.cookie_group,
            name="foo",
        )

    def test_get_cookie_group(self):
        self.assertEqual(get_cookie_group("optional"), self.cookie_group)

    def test_get_cookie(self):
        cookie_group = get_cookie_group("optional")
        self.assertEqual(get_cookie(cookie_group, "foo", ""), self.cookie)

    def test_caching(self):
        CookieGroup.objects.create(
            varname="foo",
            name="Foo",
        )
        with self.assertNumQueries(2):
            cookie_group = get_cookie_group("optional")
            get_cookie_group("foo")
            get_cookie(cookie_group, "foo", "")

    def test_caching_expire(self):
        with self.assertNumQueries(2):
            cookie_group = get_cookie_group("optional")

        self.cookie_group.name = "Bar"
        self.cookie_group.save()

        with self.assertNumQueries(2):
            cookie_group = get_cookie_group("optional")
        self.assertEqual(cookie_group.name, "Bar")

    @override_settings(
        CACHES={"tests": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}},
        COOKIE_CONSENT_CACHE_BACKEND="tests",
    )
    def test_can_override_cache_settings(self):
        """
        Assert that the cache backend/settings can be swapped out in tests.

        Regression test for #41
        """
        CookieGroup.objects.create(
            varname="foo",
            name="Foo",
        )
        # expect multiple calls to not be cached because of the no-op cache
        with self.assertNumQueries(2 + 2):
            get_cookie_group("optional")
            get_cookie_group("foo")
