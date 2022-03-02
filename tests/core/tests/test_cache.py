# -*- coding: utf-8 -*-
from django.test import (
    TestCase,
)

from cookie_consent.models import (
    Cookie,
    CookieGroup,
)
from cookie_consent.cache import (
    get_cookie_group,
    get_cookie,
)


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
