=====================
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

The latest version of Django cookie consent is available at https://github.com/bmihelac/django-cookie-consent/

User Guide
----------

.. toctree::
   :maxdepth: 2

   installation
   configuration
   concept
   getting_started
   example_app
   settings
   contributing
   changelog

API documentation
-----------------

.. toctree::
   :maxdepth: 2

   api_models
   api_views
   api_util
   api_templatetags
   api_middleware
