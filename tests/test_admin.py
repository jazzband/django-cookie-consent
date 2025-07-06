from django.test import Client
from django.urls import reverse

import pytest
from pytest_django.asserts import assertContains

from cookie_consent.models import CookieGroup

pytestmark = pytest.mark.django_db


def test_warning_icon_for_missing_cookies(
    admin_client: Client,
    required_cookiegroup: CookieGroup,
    optional_cookiegroup: CookieGroup,
):
    optional_cookiegroup.cookie_set.all().delete()

    admin_list_response = admin_client.get(
        reverse("admin:cookie_consent_cookiegroup_changelist")
    )

    assert admin_list_response.status_code == 200
    assertContains(admin_list_response, "admin/img/icon-alert", count=1)
