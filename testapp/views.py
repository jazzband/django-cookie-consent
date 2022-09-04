# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from cookie_consent.util import get_cookie_value_from_request


class TestPageView(TemplateView):
    template_name = "test_page.html"

    def get(self, request, *args, **kwargs):
        response = super(TestPageView, self).get(request, *args, **kwargs)
        if get_cookie_value_from_request(request, "optional") is True:
            val = "optional cookie set from django"
            response.set_cookie("optional_test_cookie", val)
        return response
