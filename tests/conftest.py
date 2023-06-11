import pytest

from cookie_consent.models import Cookie, CookieGroup


@pytest.fixture
def required_cookiegroup(db):
    group = CookieGroup.objects.create(
        varname="required",
        name="Functional cookies",
        is_required=True,
        is_deletable=False,
    )
    Cookie.objects.create(cookiegroup=group, name="sessionid")
    return group


@pytest.fixture
def optional_cookiegroup(db):
    group = CookieGroup.objects.create(
        varname="optional",
        name="Optional cookies",
        is_required=False,
        is_deletable=True,
    )
    Cookie.objects.create(cookiegroup=group, name="evil-tracking")
    return group
