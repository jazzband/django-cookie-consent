from unittest import mock

from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse

from cookie_consent.middleware import CleanCookiesMiddleware
from cookie_consent.models import Cookie, CookieGroup


class MiddlewareDeclineTest(TestCase):
    def setUp(self):
        def get_response(request):
            response = mock.MagicMock()
            return response

        self.middleware = CleanCookiesMiddleware(get_response)

        self.cookie_group = CookieGroup.objects.create(
            varname="optional",
            name="Optional (test) cookies",
        )
        self.cookie = Cookie.objects.create(
            cookiegroup=self.cookie_group,
            name="optional_test_cookie",
            domain="127.0.0.1",
            path="/",
        )

    def test_middleware_decline(self):
        # Accept optional cookie
        response = self.client.post(
            reverse("cookie_consent_accept", kwargs={"varname": "optional"}),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, '<span class="cookie-consent-accepted">Accepted</span>'
        )

        # Check if optional cookie accepted
        url = reverse("test_page")
        response = self.client.get(url)
        self.assertContains(response, '"optional" cookies accepted')
        self.assertEqual(
            self.client.cookies.get("optional_test_cookie").value,
            "optional cookie set from django",
        )

        # Decline optional cookie
        response = self.client.post(
            reverse("cookie_consent_decline", kwargs={"varname": "optional"}),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, '<span class="cookie-consent-declined">Declined</span>'
        )

        # Check if optional cookie declined
        url = reverse("test_page")
        response = self.client.get(url)
        self.assertContains(response, '"optional" cookies declined')
        self.assertFalse(
            self.client.cookies.get("optional_test_cookie").value,
            "optional cookie set from django",
        )

        # Test the middleware
        factory = RequestFactory()
        request = factory.get(url)
        self.middleware.__call__(request)

        print(self.client.cookies)

        self.assertEqual(self.client.cookies.get("optional_test_cookie").value, "")


class MiddlewareDeleteTest(TestCase):
    def setUp(self):
        def get_response(request):
            response = mock.MagicMock()
            return response

        self.middleware = CleanCookiesMiddleware(get_response)

        self.cookie_group = CookieGroup.objects.create(
            varname="optional",
            name="Optional (test) cookies",
        )
        self.cookie = Cookie.objects.create(
            cookiegroup=self.cookie_group,
            name="optional_test_cookie",
            domain="127.0.0.1",
            path="/",
        )

    def test_middleware_delete(self):
        # Accept optional cookie
        response = self.client.post(
            reverse("cookie_consent_accept", kwargs={"varname": "optional"}),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, '<span class="cookie-consent-accepted">Accepted</span>'
        )

        # Check if optional cookie accepted
        url = reverse("test_page")
        response = self.client.get(url)
        self.assertContains(response, '"optional" cookies accepted')
        self.assertEqual(
            self.client.cookies.get("optional_test_cookie").value,
            "optional cookie set from django",
        )

        # Delete cookie_consent cookie
        url = reverse("cookie_consent_cookie_group_list")
        response = self.client.get(url)
        cookie_consent_key = self.client.cookies.get("cookie_consent", None).key
        del self.client.cookies["cookie_consent"]

        # Check if cookie_consent cookie is deleted
        url = reverse("test_page")
        response = self.client.get(url)
        self.assertContains(response, '"optional" cookies not accepted or declined')

        factory = RequestFactory()
        request = factory.get(url)
        self.middleware.__call__(request)

        print(self.client.cookies)

        self.assertEqual(self.client.cookies.get("optional_test_cookie").value, "")
