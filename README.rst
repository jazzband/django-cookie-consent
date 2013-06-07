=====================
django-cookie-consent
=====================

Install
-------

::

    pip install django-cookie-consent

Setup
-----

Add ``coookie_consent`` to ``INSTALLED_APPS``.

Add ``django.core.context_processors.request`` to ``TEMPLATE_CONTEXT_PROCESSORS``.

Include cookie consent urls in ``urls.py``::

    url(r'^cookies/', include('cookie_consent.urls')),


TODO
----

No raising exception if cookie oes not exists
