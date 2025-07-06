from django.views.generic import TemplateView

from cookie_consent.util import get_cookie_value_from_request


class TestPageView(TemplateView):
    template_name = "test_page.html"

    def _should_set_cookie(self) -> bool:
        if "force" in self.request.GET:
            return True

        cookie_value = get_cookie_value_from_request(self.request, "optional")
        return cookie_value is True

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if self._should_set_cookie():
            val = "optional cookie set from django"
            response.set_cookie("optional_test_cookie", val)
        return response
