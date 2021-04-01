# -*- coding: utf-8 -*-
from __future__ import unicode_literals
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import (
    ListView,
    View,
)
from django.views.generic.edit import FormView

from .forms import CookieGroupForm
from .models import (
    CookieGroup, ACTION_DECLINED, ACTION_ACCEPTED
)
from .util import (
    accept_cookies,
    decline_cookies,
    accept_and_decline_cookies,
)


class CookieGroupListView(ListView):
    """
    Display all cookies.
    """
    model = CookieGroup


class CookieGroupBaseProcessView(View):

    def get_success_url(self):
        """
        If user adds a 'next' as URL parameter or hidden input, 
        redirect to the value of 'next'. Otherwise, redirect to 
        cookie consent group list
        """
        return (
            self.request.POST.get('next') or self.request.GET.get(
                'next', reverse('cookie_consent_cookie_group_list')
            )
	    )


    def process(self, request, response, varname):
        raise NotImplementedError()

    def post(self, request, *args, **kwargs):
        varname = kwargs.get('varname', None)
        if request.is_ajax():
            response = HttpResponse()
        else:
            response = HttpResponseRedirect(self.get_success_url())
        self.process(request, response, varname)
        return response

    def get(self, request, *args, **kwargs):
        varname = kwargs.get('varname', None)
        if request.is_ajax():
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


class CookieGroupFormView(FormView):
    template_name = "cookie_consent/cookiegroup_list.html"
    form_class = CookieGroupForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)

        if form.is_valid():
            cleaned_data = form.cleaned_data
            declined_cookie_groups = ",".join([key for key, val in cleaned_data.items() if val == ACTION_DECLINED])
            accepted_cookie_groups = ",".join([key for key, val in cleaned_data.items() if val == ACTION_ACCEPTED])
            accept_and_decline_cookies(self.request, response, accepted_cookie_groups, declined_cookie_groups)

        return response

    def get_success_url(self):
        return self.request.GET.get("next", "/")
