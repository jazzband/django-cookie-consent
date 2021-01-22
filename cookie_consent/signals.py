import django.dispatch

accept_cookie = django.dispatch.Signal(providing_args=["cookie_group", "request", "action"])
decline_cookie = django.dispatch.Signal(providing_args=["cookie_group", "request", "action"])
