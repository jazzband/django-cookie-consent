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
        self.widget = CookieGroupWidget({"cookie_group": self.cookie_group, "initial": self.initial})
        super().__init__(*args, **kwargs)


class CookieGroupForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        initials = self._get_form_initials()
        for cookie_group in CookieGroup.objects.all():
            self.fields[cookie_group.varname] = CookieGroupField(
                cookie_group=cookie_group,
                required=False,
                initial=initials.get(cookie_group.varname),
                label=False,
            )

    def _get_form_initials(self):
        accepted_cookie_groups = get_accepted_cookie_groups(self.request)
        not_accepeted_or_declined_cookie_groups = get_not_accepted_or_declined_cookie_groups(self.request)

        initial = {}
        for cookie_group in CookieGroup.objects.all():
            action = ACTION_DECLINED

            if (cookie_group.varname in accepted_cookie_groups) or cookie_group.is_required:
                action = ACTION_ACCEPTED
            elif cookie_group in not_accepeted_or_declined_cookie_groups:
                action = None

            initial[cookie_group.varname] = action

        return initial

    def clean(self):
        # The checkbox typpe won't send any value if not checked. We need to set a cookie group to -1 if not in the request.POST
        cleaned_data = super().clean()
        cookie_groups = CookieGroup.objects.values_list("varname", flat=True)
        declined_cookie_groups = set(cookie_groups) - set(cleaned_data.keys())
        cleaned_data.update({cookie_group: ACTION_DECLINED for cookie_group in declined_cookie_groups})
        return cleaned_data
