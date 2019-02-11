Django cookie consent
=====================

django-cookie-consent is a reusable application for managing various
cookies and visitors consent for their use in Django project.

Features:

* cookies and cookie groups are stored in models for easy management
  through Django admin interface

* support for both opt-in and opt-out cookie consent schemes

* removing declined cookies (or non accepted when opt-in scheme is used)

* logging user actions when they accept and decline various cookies

* easy adding new cookies and seamlessly re-asking for consent for new cookies

Documentation
-------------

https://django-cookie-consent.readthedocs.org/en/latest/


Configuration
-------------

1. Add ``cookie_consent`` to your ``INSTALLED_APPS``.

2. Add ``django.template.context_processors.request``
   to ``TEMPLATE_CONTEXT_PROCESSORS`` if it is not already added.

3. Include django-cookie-consent urls in ``urls.py``::

    url(r'^cookies/', include('cookie_consent.urls'))

4. Run ``migrate`` django management command.


Example app
-----------

::

    cd tests && ./manage.py runserver

Username and password for admin are 'admin', 'password'.
