# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from .models import CookieGroup, ACTION_DECLINED, ACTION_ACCEPTED
from .util import get_accepted_cookie_groups, get_not_accepted_or_declined_cookie_groups
from .widgets import CookieGroupWidget


class CookieGroupField(forms.IntegerField):
    def __init__(self, *args, **kwargs):
        self.cookie_group = kwargs.pop("cookie_group")
        self.initial = kwargs.pop("initial")
        self.widget = CookieGroupWidget({"initial": self.initial, "cookie_group": self.cookie_group})
        super().__init__(*args, **kwargs)


class CookieGroupForm(forms.Form):
    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

        accepted_cookie_groups = get_accepted_cookie_groups(request)
        not_accepeted_or_declined_cookie_groups = get_not_accepted_or_declined_cookie_groups(request)

        for cookie_group in CookieGroup.objects.all():
            initial = ACTION_DECLINED

            if (cookie_group.varname in accepted_cookie_groups) or cookie_group.is_required:
                initial = ACTION_ACCEPTED
            elif cookie_group in not_accepeted_or_declined_cookie_groups:
                initial = None

            self.fields[f"{cookie_group.varname}"] = CookieGroupField(initial=initial, cookie_group=cookie_group)

    @property
    def cookie_group_fields(self):
        for field_name in self.fields:
            yield self[field_name]
