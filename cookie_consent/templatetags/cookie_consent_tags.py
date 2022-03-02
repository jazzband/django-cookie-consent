# -*- coding: utf-8 -*-
from django import template
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

from cookie_consent.util import (
    get_accepted_cookies,
    get_cookie_string,
    get_cookie_value_from_request,
    get_cookie_dict_from_request,
    are_all_cookies_accepted,
    get_not_accepted_or_declined_cookie_groups,
    is_cookie_consent_enabled,
)
from cookie_consent.conf import settings


register = template.Library()


@register.filter
def cookie_group_accepted(request, arg):
    """
    Filter returns if cookie group is accepted.

    Examples:
    ::

        {{ request|cookie_group_accepted:"analytics" }}
        {{ request|cookie_group_accepted:"analytics=*:.google.com" }}
    """
    value = get_cookie_value_from_request(request, *arg.split("="))
    return value is True


@register.filter
def cookie_group_declined(request, arg):
    """
    Filter returns if cookie group is declined.
    """
    value = get_cookie_value_from_request(request, *arg.split("="))
    return value is False


@register.filter
def all_cookies_accepted(request):
    """
    Filter returns if all cookies are accepted.
    """
    return are_all_cookies_accepted(request)


@register.simple_tag
def not_accepted_or_declined_cookie_groups(request):
    """
    Assignement tag returns cookie groups that does not yet given consent
    or decline.
    """
    return get_not_accepted_or_declined_cookie_groups(request)


@register.filter
def cookie_consent_enabled(request):
    """
    Filter returns if cookie consent enabled for this request.
    """
    return is_cookie_consent_enabled(request)


@register.simple_tag
def cookie_consent_accept_url(cookie_groups):
    """
    Assignement tag returns url for accepting given concept groups.
    """
    varnames = ",".join([g.varname for g in cookie_groups])
    url = reverse("cookie_consent_accept", kwargs={"varname": varnames})
    return url


@register.simple_tag
def cookie_consent_decline_url(cookie_groups):
    """
    Assignement tag returns url for declining given concept groups.
    """
    varnames = ",".join([g.varname for g in cookie_groups])
    url = reverse("cookie_consent_decline", kwargs={"varname": varnames})
    return url


@register.simple_tag
def get_accept_cookie_groups_cookie_string(request, cookie_groups):
    """
    Tag returns accept cookie string suitable to use in javascript.
    """
    cookie_dic = get_cookie_dict_from_request(request)
    for cookie_group in cookie_groups:
        cookie_dic[cookie_group.varname] = cookie_group.get_version()
    return get_cookie_string(cookie_dic)


@register.simple_tag
def get_decline_cookie_groups_cookie_string(request, cookie_groups):
    """
    Tag returns decline cookie string suitable to use in javascript.
    """
    cookie_dic = get_cookie_dict_from_request(request)
    for cookie_group in cookie_groups:
        cookie_dic[cookie_group.varname] = settings.COOKIE_CONSENT_DECLINE
    return get_cookie_string(cookie_dic)


@register.simple_tag
def js_type_for_cookie_consent(request, varname, cookie=None):
    """
    Tag returns "x/cookie_consent" when processing javascript
    will create an cookie and consent does not exists yet.

    Example::

      <script type="{% js_type_for_cookie_consent request "social" %}"
      data-varname="social">
        alert("Social cookie accepted");
      </script>
    """
    enabled = is_cookie_consent_enabled(request)
    if not enabled:
        res = True
    else:
        value = get_cookie_value_from_request(request, varname, cookie)
        if value is None:
            res = settings.COOKIE_CONSENT_OPT_OUT
        else:
            res = value
    return "text/javascript" if res else "x/cookie_consent"


@register.filter
def accepted_cookies(request):
    """
    Filter returns accepted cookies varnames.

    ::
        {{ request|accepted_cookies }}
    """
    return [c.varname for c in get_accepted_cookies(request)]
