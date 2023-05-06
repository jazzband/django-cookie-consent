from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CookieConsentConf(AppConfig):
    name = "cookie_consent"
    verbose_name = _("cookie consent")
    default_auto_field = "django.db.models.AutoField"
