from django import forms


class CookieGroupWidget(forms.Widget):
    template_name = "cookie_consent/cookie_group_widget.html"
