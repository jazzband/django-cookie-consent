from django.urls import reverse

import pytest

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    ("setting", "value", "assertion"),
    [
        ("MAX_AGE", 3600, {"max-age": 3600}),
        ("DOMAIN", None, {"domain": ""}),
        ("DOMAIN", "example.com", {"domain": "example.com"}),
        ("SECURE", True, {"secure": True}),
        ("SECURE", False, {"secure": ""}),
        ("SECURE", None, {"secure": ""}),
        ("HTTPONLY", True, {"httponly": True}),
        ("HTTPONLY", None, {"httponly": ""}),
        ("HTTPONLY", False, {"httponly": ""}),
        ("SAMESITE", "Lax", {"samesite": "Lax"}),
        ("SAMESITE", None, {"samesite": ""}),
        ("SAMESITE", False, {"samesite": ""}),
        ("SAMESITE", "None", {"samesite": "None"}),
        ("SAMESITE", "Strict", {"samesite": "Strict"}),
    ],
)
def test_cookie_consent_cookie_options(settings, client, setting, value, assertion):
    accept_all_url = reverse("cookie_consent_accept_all")
    setattr(settings, f"COOKIE_CONSENT_{setting}", value)

    client.post(accept_all_url)

    cookie = client.cookies[settings.COOKIE_CONSENT_NAME]
    for key, expected in assertion.items():
        assert cookie[key] == expected
