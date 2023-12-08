# -*- coding: utf-8 -*-
from unittest import mock

from django.core.exceptions import ValidationError
from django.test import TestCase

from cookie_consent.cache import delete_cache
from cookie_consent.models import Cookie, CookieGroup, validate_cookie_name


class CookieGroupTest(TestCase):
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

    @mock.patch("cookie_consent.models.delete_cache")
    def test_bulk_delete(self, mock_delete_cache):
        deleted_objs_count, _ = CookieGroup.objects.filter(
            id=self.cookie_group.id
        ).delete()

        # Deleting a CookieGroup also deletes the associated Cookies, that's why we expect a count of 2.
        self.assertEqual(deleted_objs_count, 2)
        self.assertEqual(mock_delete_cache.call_count, 1)

    @mock.patch("cookie_consent.models.delete_cache")
    def test_bulk_update(self, mock_delete_cache):
        updated_objs_count = CookieGroup.objects.filter(id=self.cookie_group.id).update(
            name="Optional2"
        )

        self.assertEqual(updated_objs_count, 1)
        self.assertEqual(mock_delete_cache.call_count, 1)


class CookieTest(TestCase):
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

    @mock.patch("cookie_consent.models.delete_cache")
    def test_bulk_delete(self, mock_delete_cache):
        deleted_objs_count, _ = Cookie.objects.filter(id=self.cookie.id).delete()

        self.assertEqual(deleted_objs_count, 1)
        self.assertEqual(mock_delete_cache.call_count, 1)

    @mock.patch("cookie_consent.models.delete_cache")
    def test_bulk_update(self, mock_delete_cache):
        updated_objs_count = Cookie.objects.filter(id=self.cookie.id).update(
            name="foo2"
        )

        self.assertEqual(updated_objs_count, 1)
        self.assertEqual(mock_delete_cache.call_count, 1)


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
