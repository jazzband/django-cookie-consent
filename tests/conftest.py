import os
from io import StringIO
from pathlib import Path

from django.core.management import call_command

import pytest

from cookie_consent.cache import delete_cache
from cookie_consent.models import Cookie, CookieGroup

TEST_APP_DIR = Path(__file__).parent.parent.resolve() / "testapp"

# otherwise pytest-playwright and pytest-django don't play nice :(
# See https://github.com/microsoft/playwright-pytest/issues/46
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "1"


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


@pytest.fixture
def load_testapp_fixture(transactional_db):
    fixture = str(TEST_APP_DIR / "fixture.json")
    call_command("loaddata", fixture, stdout=StringIO())


@pytest.fixture(scope="function", autouse=True)
def before_each_after_each():
    yield
    delete_cache()
