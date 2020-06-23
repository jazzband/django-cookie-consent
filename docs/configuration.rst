=============
Configuration
=============

1. Add ``cookie_consent`` to your ``INSTALLED_APPS``.

2. Add ``django.template.context_processors.request``
   to ``TEMPLATE_CONTEXT_PROCESSORS`` if it is not already added.

3. Include django-cookie-consent urls in ``urls.py``::

    path('cookies/', include('cookie_consent.urls'))
    # or for older Django versions:
    url(r'^cookies/', include('cookie_consent.urls'))

4. Add ``COOKIE_CONSENT_NAME`` and ``COOKIE_CONSENT_MAX_AGE`` under ``settings.py``::
   
    COOKIE_CONSENT_NAME = "cookie_consent"
    COOKIE_CONSENT_MAX_AGE = 60 * 60 * 24 * 365 * 1  # 1 year
   

5. Run ``syncdb`` or ``migrate`` django management command.
