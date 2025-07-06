from django.test import Client, TestCase
from django.test.utils import override_settings
from django.urls import reverse

import pytest
from pytest_django.asserts import assertRedirects

from cookie_consent.models import (
    ACTION_ACCEPTED,
    ACTION_DECLINED,
    Cookie,
    CookieGroup,
    LogItem,
)


@pytest.mark.django_db
def test_processing_get_success_url(client: Client):
    """
    If user adds a 'next' as URL parameter it should,
    redirect to the value of 'next'
    """
    expected_url = reverse("test_page")
    url = "{}?next={}".format(reverse("cookie_consent_accept_all"), expected_url)

    response = client.post(url, follow=True)

    assertRedirects(response, expected_url)


@pytest.mark.django_db
def test_processing_no_open_redirects(client: Client):
    url = "{}?next=https://evil.com".format(reverse("cookie_consent_accept_all"))

    response = client.post(url, follow=True)

    assert response.status_code == 400  # result of SupiciousOperation


@pytest.mark.django_db
def test_alternative_redirect_fallback(client: Client, settings):
    settings.COOKIE_CONSENT_SUCCESS_URL = "/alternative"

    response = client.post(reverse("cookie_consent_accept_all"), follow=False)

    assertRedirects(response, "/alternative", fetch_redirect_response=False)


class IntegrationTest(TestCase):
    def setUp(self):
        self.cookie_group = CookieGroup.objects.create(
            varname="optional",
            name="Optional",
        )
        self.cookie = Cookie.objects.create(
            cookiegroup=self.cookie_group,
            name="foo",
        )

    def test_cookies_view(self):
        response = self.client.get(reverse("cookie_consent_cookie_group_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<input type="submit" value="Accept">')
        self.assertContains(response, '<input type="submit" value="Decline">')

    def test_accept_cookie(self):
        response = self.client.post(
            reverse("cookie_consent_accept", kwargs={"varname": "optional"}),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, '<span class="cookie-consent-accepted">Accepted</span>'
        )

    def test_accept_cookie_ajax(self):
        response = self.client.post(
            reverse("cookie_consent_accept", kwargs={"varname": "optional"}),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 200)

    def test_decline_cookie(self):
        response = self.client.post(
            reverse("cookie_consent_decline", kwargs={"varname": "optional"}),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, '<span class="cookie-consent-declined">Declined</span>'
        )

    def test_decline_cookie_ajax(self):
        response = self.client.delete(
            reverse("cookie_consent_decline", kwargs={"varname": "optional"}),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 200)

    def test_cookies(self):
        CookieGroup.objects.create(
            varname="social",
            name="Social",
        )
        Cookie.objects.create(
            cookiegroup=self.cookie_group,
            name="optional_test_cookie",
        )

        url = reverse("test_page")
        response = self.client.get(url)
        self.assertContains(response, '"optional" cookies not accepted or declined')

        response = self.client.post(
            reverse("cookie_consent_accept", kwargs={"varname": "optional"})
        )
        response = self.client.get(url)
        self.assertContains(response, '"optional" cookies accepted')
        self.assertEqual(
            self.client.cookies.get("optional_test_cookie").value,
            "optional cookie set from django",
        )

        response = self.client.post(
            reverse("cookie_consent_decline", kwargs={"varname": "optional"})
        )
        response = self.client.get(url)
        self.assertContains(response, '"optional" cookies declined')
        # test client returns cookie with value of ''
        # self.assertIsNone(self.client.cookies.get('optional_test_cookie'))
        self.assertFalse(self.client.cookies.get("optional_test_cookie").value)

    def test_logging(self):
        self.client.post(
            reverse("cookie_consent_accept", kwargs={"varname": "optional"})
        )
        log_items = LogItem.objects.filter(
            cookiegroup=self.cookie_group,
            version=self.cookie_group.get_version(),
            action=ACTION_ACCEPTED,
        )
        self.assertEqual(log_items.count(), 1)

        self.client.delete(
            reverse("cookie_consent_decline", kwargs={"varname": "optional"})
        )
        log_items = LogItem.objects.filter(
            cookiegroup=self.cookie_group,
            version=self.cookie_group.get_version(),
            action=ACTION_DECLINED,
        )
        self.assertEqual(log_items.count(), 1)

    @override_settings(COOKIE_CONSENT_LOG_ENABLED=False)
    def test_logging_disabled(self):
        """
        When the COOKIE_CONSENT_LOG_ENABLED is False, no log item should be
        created
        """
        self.client.post(
            reverse("cookie_consent_accept", kwargs={"varname": "optional"})
        )
        log_items = LogItem.objects.filter(
            cookiegroup=self.cookie_group,
            version=self.cookie_group.get_version(),
            action=ACTION_ACCEPTED,
        )
        self.assertEqual(log_items.count(), 0)

        self.client.delete(
            reverse("cookie_consent_decline", kwargs={"varname": "optional"})
        )
        log_items = LogItem.objects.filter(
            cookiegroup=self.cookie_group,
            version=self.cookie_group.get_version(),
            action=ACTION_DECLINED,
        )
        self.assertEqual(log_items.count(), 0)
