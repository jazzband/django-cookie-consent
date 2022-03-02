Django cookie consent
=====================

[![Build Status](https://travis-ci.com/bmihelac/django-cookie-consent.svg?branch=master)](https://travis-ci.com/bmihelac/django-cookie-consent)
![PyPI - License](https://img.shields.io/pypi/l/django-cookie-consent)
[![PyPI](https://img.shields.io/pypi/v/django-cookie-consent)](https://pypi.python.org/pypi/django-cookie-consent)
![PyPI](https://img.shields.io/pypi/pyversions/django-cookie-consent)
![PyPI](https://img.shields.io/pypi/djversions/django-cookie-consent)


django-cookie-consent is a reusable application for managing various
cookies and visitors consent for their use in Django project.

Support ranges from django 2.2 to 4.0 and python 3.6 to 3.9

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

Username and password for admin are 'administrator', 'password'.
