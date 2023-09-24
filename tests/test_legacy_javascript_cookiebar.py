"""
These tests mostly exist to assert code coverage while giving library users time
to transition to the new implementation.

TODO: remove in django-cookie-consent 1.0
"""
from django.urls import reverse

import pytest
from playwright.sync_api import Page, expect

pytestmark = [pytest.mark.django_db, pytest.mark.e2e]


COOKIE_BAR_CONTENT = """
This site uses Social, Optional cookies for better performance and user experience.
Do you agree to use cookies?
"""


@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(live_server, page: Page, load_testapp_fixture):
    test_page_url = f"{live_server.url}{reverse('legacy_test_page')}"
    page.goto(test_page_url)
    yield


def test_cookiebar_shows_initially(page: Page):
    cookiebar = page.get_by_text(COOKIE_BAR_CONTENT)
    expect(cookiebar).to_be_visible()


def test_cookiebar_accept_all(page: Page):
    accept_link = page.get_by_role("link", name="Accept")
    expect(accept_link).to_be_visible()

    accept_link.click()

    expect(page.get_by_text(COOKIE_BAR_CONTENT)).not_to_be_visible()
    share_button = page.get_by_role("button", name="SHARE")
    expect(share_button).to_be_visible()


def test_cookiebar_decline_all(page: Page):
    decline_link = page.get_by_role("link", name="Decline")
    expect(decline_link).to_be_visible()

    decline_link.click()

    expect(page.get_by_text(COOKIE_BAR_CONTENT)).not_to_be_visible()
    share_button = page.get_by_role("button", name="SHARE")
    expect(share_button).not_to_be_visible()


@pytest.mark.parametrize("btn_text", ["Accept", "Decline"])
def test_cookiebar_not_shown_anymore_after_accept_or_decline(btn_text: str, page: Page):
    expect(page.get_by_text(COOKIE_BAR_CONTENT)).to_be_visible()

    link = page.get_by_role("link", name=btn_text)
    expect(link).to_be_visible()

    link.click()
    expect(page.get_by_text(COOKIE_BAR_CONTENT)).not_to_be_visible()

    page.reload()
    expect(page.get_by_text(COOKIE_BAR_CONTENT)).not_to_be_visible()


def test_on_accept_handler_runs_on_load(page: Page, live_server):
    accept_link = page.get_by_role("link", name="Accept")
    accept_link.click()

    test_page_url = f"{live_server.url}{reverse('legacy_test_page')}"
    page.goto(test_page_url)

    share_button = page.get_by_role("button", name="SHARE")
    expect(share_button).to_be_visible()
