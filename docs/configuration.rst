=============
Configuration
=============

1. Add ``cookie_consent`` to your ``INSTALLED_APPS``.

2. Add ``django.core.context_processors.request``
   to ``TEMPLATE_CONTEXT_PROCESSORS`` if it is not already added.

3. Include django-cookie-consent urls in ``urls.py``::

    url(r'^cookies/', include('cookie_consent.urls'))

4. Run ``syncdb`` or ``migrate`` django management command.
