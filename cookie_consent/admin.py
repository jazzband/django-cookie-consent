from django.contrib import admin
from django.db.models import Count
from django.templatetags.l10n import localize
from django.templatetags.static import static
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .conf import settings
from .models import Cookie, CookieGroup, LogItem


class CookieAdmin(admin.ModelAdmin):
    list_display = ("varname", "name", "cookiegroup", "path", "domain", "get_version")
    search_fields = ("name", "domain", "cookiegroup__varname", "cookiegroup__name")
    readonly_fields = ("varname",)
    list_filter = ("cookiegroup",)


class CookieGroupAdmin(admin.ModelAdmin):
    list_display = (
        "varname",
        "name",
        "is_required",
        "is_deletable",
        "num_cookies",
        "get_version",
    )
    search_fields = (
        "varname",
        "name",
    )
    list_filter = (
        "is_required",
        "is_deletable",
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(num_cookies=Count("cookie"))

    @admin.display(ordering="num_cookies", description=_("# cookies"))
    def num_cookies(self, obj):
        if (count := obj.num_cookies) > 0:
            return localize(count)

        return format_html(
            '{count} <img src="{src}" alt="{alt}">',
            count=localize(count),
            src=static("admin/img/icon-alert.svg"),
            alt=_("Warning icon for missing cookies in cookie group."),
        )


class LogItemAdmin(admin.ModelAdmin):
    list_display = ("action", "cookiegroup", "version", "created")
    list_filter = ("action", "cookiegroup")
    readonly_fields = ("action", "cookiegroup", "version", "created")
    date_hierarchy = "created"


admin.site.register(Cookie, CookieAdmin)
admin.site.register(CookieGroup, CookieGroupAdmin)
if settings.COOKIE_CONSENT_LOG_ENABLED:
    admin.site.register(LogItem, LogItemAdmin)
