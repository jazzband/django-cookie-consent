# -*- coding: utf-8 -*-
import re

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

from cookie_consent.cache import delete_cache


COOKIE_NAME_RE = re.compile(r'^[-_a-zA-Z0-9]+$')
validate_cookie_name = RegexValidator(
    COOKIE_NAME_RE,
    _(u"Enter a valid 'varname' consisting of letters, numbers"
      ", underscores or hyphens."),
    'invalid')


class CookieGroup(models.Model):
    varname = models.CharField(
        _('Variable name'),
        max_length=32,
        validators=[validate_cookie_name])
    name = models.CharField(_('Name'), max_length=100, blank=True)
    description = models.TextField(_('Description'), blank=True)
    is_required = models.BooleanField(
        _('Is required'),
        help_text=_('Are cookies in this group required.'),
        default=False)
    is_deletable = models.BooleanField(
        _('Is deletable?'),
        help_text=_('Can cookies in this group be deleted.'),
        default=True)
    ordering = models.IntegerField(_('Ordering'), default=0)
    created = models.DateTimeField(_('Created'), auto_now_add=True, blank=True)

    class Meta:
        verbose_name = _('Cookie Group')
        verbose_name_plural = _('Cookie Groups')
        ordering = ['ordering']

    def __str__(self):
        return self.name

    def get_version(self):
        try:
            return str(self.cookie_set.all()[0].get_version())
        except IndexError:
            return ""

    def delete(self, *args, **kwargs):
        super(CookieGroup, self).delete(*args, **kwargs)
        delete_cache()

    def save(self, *args, **kwargs):
        super(CookieGroup, self).save(*args, **kwargs)
        delete_cache()


class Cookie(models.Model):
    cookiegroup = models.ForeignKey(
        CookieGroup,
        verbose_name=CookieGroup._meta.verbose_name,
        on_delete=models.CASCADE)
    name = models.CharField(_('Name'), max_length=250)
    description = models.TextField(_('Description'), blank=True)
    path = models.TextField(_('Path'), blank=True, default="/")
    domain = models.CharField(_('Domain'), max_length=250, blank=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True, blank=True)

    class Meta:
        verbose_name = _('Cookie')
        verbose_name_plural = _('Cookies')
        ordering = ['-created']

    def __str__(self):
        return "%s %s%s" % (self.name, self.domain, self.path)

    @property
    def varname(self):
        return "%s=%s:%s" % (self.cookiegroup.varname, self.name, self.domain)

    def get_version(self):
        return self.created.isoformat()

    def delete(self, *args, **kwargs):
        super(Cookie, self).delete(*args, **kwargs)
        delete_cache()

    def save(self, *args, **kwargs):
        super(Cookie, self).save(*args, **kwargs)
        delete_cache()


ACTION_ACCEPTED = 1
ACTION_DECLINED = -1
ACTION_CHOICES = (
    (ACTION_DECLINED, _('Declined')),
    (ACTION_ACCEPTED, _('Accepted')),
)


class LogItem(models.Model):
    action = models.IntegerField(_('Action'), choices=ACTION_CHOICES)
    cookiegroup = models.ForeignKey(
        CookieGroup,
        verbose_name=CookieGroup._meta.verbose_name,
        on_delete=models.CASCADE)
    version = models.CharField(_('Version'), max_length=32)
    created = models.DateTimeField(_('Created'), auto_now_add=True, blank=True)
    def __str__(self):
        return "%s %s" % (self.cookiegroup.name, self.version)

    class Meta:
        verbose_name = _('Log item')
        verbose_name_plural = _('Log items')
        ordering = ['-created']
