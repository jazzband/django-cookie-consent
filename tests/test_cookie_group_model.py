import pytest

from cookie_consent.models import CookieGroup


def test_natural_key():
    group = CookieGroup(varname="social")

    assert group.natural_key() == ("social",)


@pytest.mark.django_db
def test_load_by_natural_key():
    social_group = CookieGroup.objects.create(varname="social")
    CookieGroup.objects.create(varname="other")

    loaded_group = CookieGroup.objects.get_by_natural_key("social")

    assert loaded_group == social_group
