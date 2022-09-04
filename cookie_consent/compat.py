try:
    from django.utils.http import url_has_allowed_host_and_scheme
except ImportError:  # django < 3.0
    from django.utils.http import is_safe_url as url_has_allowed_host_and_scheme

try:  # django >= 4.1
    from django.contrib.auth.views import RedirectURLMixin
except ImportError:
    from django.contrib.auth.views import (
        SuccessURLAllowedHostsMixin as RedirectURLMixin,
    )
