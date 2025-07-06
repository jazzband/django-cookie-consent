from textwrap import dedent
from typing import Any

from django.template import Context, Template

import pytest


def render(tpl: str, context: dict[str, Any] | None = None) -> str:
    template = Template(dedent(tpl).strip())
    return template.render(Context(context))


NOT_ACCEPT_OR_DECLINED_TEMPLATE = """
{% load cookie_consent_tags %}
{% not_accepted_or_declined_cookie_groups request as cookie_groups %}
{% if cookie_groups %}FOUND COOKIES{% else %}NO COOKIES{% endif %}
"""


@pytest.mark.django_db
def test_not_accepted_or_declined_cookie_groups_only_required_cookies(
    required_cookiegroup, rf
):
    context = {"request": rf.get("/")}

    output = render(NOT_ACCEPT_OR_DECLINED_TEMPLATE, context).strip()

    assert output == "NO COOKIES"


@pytest.mark.django_db
def test_not_accepted_or_declined_cookie_groups_only_optional_cookies(
    optional_cookiegroup, rf
):
    context = {"request": rf.get("/")}

    output = render(NOT_ACCEPT_OR_DECLINED_TEMPLATE, context).strip()

    assert output == "FOUND COOKIES"


def test_not_accepted_or_declined_cookie_groups_required_and_optional_cookies(
    required_cookiegroup, optional_cookiegroup, rf
):
    context = {"request": rf.get("/")}

    output = render(NOT_ACCEPT_OR_DECLINED_TEMPLATE, context).strip()

    assert output == "FOUND COOKIES"
