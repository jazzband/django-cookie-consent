# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.test import (
    TestCase,
)

from cookie_consent.models import (
    Cookie,
    CookieGroup,
    validate_cookie_name,
)


class CookieGroupTest(TestCase):

    def setUp(self):
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
            self.cookie_group.get_version(),
            self.cookie.created.isoformat()
        )


class CookieTest(TestCase):

    def setUp(self):
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
