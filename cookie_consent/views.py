# -*- coding: utf-8 -*-
from django.contrib.auth.views import RedirectURLMixin
from django.core.exceptions import SuspiciousOperation
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.middleware.csrf import get_token as get_csrf_token
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic import ListView, View

from .models import CookieGroup
from .util import (
    accept_cookies,
    decline_cookies,
    get_accepted_cookie_groups,
    get_declined_cookie_groups,
    get_not_accepted_or_declined_cookie_groups,
)


def is_ajax_like(request: HttpRequest) -> bool:
    # legacy ajax, removed in Django 4.0 (used to be request.is_ajax())
    ajax_header = request.headers.get("X-Requested-With")
    if ajax_header == "XMLHttpRequest":
        return True

    # module-js uses fetch and a custom header
    return bool(request.headers.get("X-Cookie-Consent-Fetch"))


class CookieGroupListView(ListView):
    """
    Display all cookies.
    """

    model = CookieGroup


class CookieGroupBaseProcessView(RedirectURLMixin, View):
    def get_success_url(self):
        """
        If user adds a 'next' as URL parameter or hidden input,
        redirect to the value of 'next'. Otherwise, redirect to
        cookie consent group list
        """
        redirect_to = self.request.POST.get("next", self.request.GET.get("next"))
        if redirect_to and not url_has_allowed_host_and_scheme(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        ):
            raise SuspiciousOperation("Unsafe open redirect suspected.")
        return redirect_to or reverse("cookie_consent_cookie_group_list")

    def process(self, request, response, varname):  # pragma: no cover
        raise NotImplementedError()

    def post(self, request, *args, **kwargs):
        varname = kwargs.get("varname", None)
        if is_ajax_like(request):
            response = HttpResponse()
        else:
            response = HttpResponseRedirect(self.get_success_url())
        self.process(request, response, varname)
        return response


class CookieGroupAcceptView(CookieGroupBaseProcessView):
    """
    View to accept CookieGroup.
    """

    def process(self, request, response, varname):
        accept_cookies(request, response, varname)


class CookieGroupDeclineView(CookieGroupBaseProcessView):
    """
    View to decline CookieGroup.
    """

    def process(self, request, response, varname):
        decline_cookies(request, response, varname)

    def delete(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class CookieStatusView(View):
    """
    Check the current accept/decline status for cookies.

    The returned accept and decline URLs are specific to this user and include the
    cookie groups that weren't accepted or declined yet.

    Note that this endpoint also returns a CSRF Token to be used by the frontend,
    as baking a CSRFToken into a cached page will not reliably work.
    """

    def get(self, request: HttpRequest) -> JsonResponse:
        accepted = get_accepted_cookie_groups(request)
        declined = get_declined_cookie_groups(request)
        not_accepted_or_declined = get_not_accepted_or_declined_cookie_groups(request)
        # TODO: change this csv URL param into proper POST params
        varnames = ",".join([group.varname for group in not_accepted_or_declined])
        data = {
            "csrftoken": get_csrf_token(request),
            "acceptUrl": reverse("cookie_consent_accept", kwargs={"varname": varnames}),
            "declineUrl": reverse(
                "cookie_consent_decline", kwargs={"varname": varnames}
            ),
            "acceptedCookieGroups": [group.varname for group in accepted],
            "declinedCookieGroups": [group.varname for group in declined],
            "notAcceptedOrDeclinedCookieGroups": [
                group.varname for group in not_accepted_or_declined
            ],
        }
        return JsonResponse(data)
