try:  # django >= 4.1
    from django.contrib.auth.views import RedirectURLMixin
except ImportError:
    from django.contrib.auth.views import (
        SuccessURLAllowedHostsMixin as RedirectURLMixin,
    )

__all__ = ["RedirectURLMixin"]
