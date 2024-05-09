import pytest

from cookie_consent.models import Cookie, CookieGroup


def test_natural_key():
    cookie = Cookie(
        cookiegroup=CookieGroup(varname="analytics"), name="trck", domain="example.com"
    )

    assert cookie.natural_key() == ("trck", "example.com", "analytics")


@pytest.mark.django_db
def test_load_by_natural_key():
    social_group = CookieGroup.objects.create(varname="social")
    cookie = Cookie.objects.create(
        cookiegroup=social_group, name="trck", domain="example.com"
    )
    Cookie.objects.create(cookiegroup=social_group, name="other", domain="example.com")

    loaded_cookie = Cookie.objects.get_by_natural_key("trck", "example.com", "social")

    assert loaded_cookie == cookie
