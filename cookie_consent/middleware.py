# -*- coding: utf-8 -*-
from django.utils.encoding import smart_str

from cookie_consent.cache import all_cookie_groups
from cookie_consent.util import (
    get_cookie_dict_from_request,
    is_cookie_consent_enabled,
)
from cookie_consent.conf import settings


class CleanCookiesMiddleware(object):
    """
    Clean declined cookies or non accepted cookies if not
    COOKIE_CONSENT_OPT_OUT set.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def process_response(self, request, response):
        if not is_cookie_consent_enabled(request):
            return response
        cookie_dic = get_cookie_dict_from_request(request)
        for cookie_group in all_cookie_groups().values():
            if not cookie_group.is_deletable:
                continue
            group_version = cookie_dic.get(cookie_group.varname, None)
            for cookie in cookie_group.cookie_set.all():
                if cookie.name not in request.COOKIES:
                    continue
                if group_version == settings.COOKIE_CONSENT_DECLINE:
                    response.delete_cookie(smart_str(cookie.name),
                                           cookie.path, cookie.domain)
                if group_version < cookie.get_version() and not settings.COOKIE_CONSENT_OPT_OUT:
                    response.delete_cookie(
                        smart_str(cookie.name),
                        cookie.path, cookie.domain
                    )
        return response
