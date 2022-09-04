# -*- coding: utf-8 -*-
from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, View

from .compat import RedirectURLMixin, url_has_allowed_host_and_scheme
from .models import CookieGroup
from .util import accept_cookies, decline_cookies


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

    def process(self, request, response, varname):
        raise NotImplementedError()

    def post(self, request, *args, **kwargs):
        varname = kwargs.get("varname", None)
        if request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
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
