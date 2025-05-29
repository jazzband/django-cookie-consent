=====================
Django cookie consent
=====================

Manage cookie information and let visitors give or reject consent for them.

|build-status| |code-quality| |black| |coverage| |docs|

|python-versions| |django-versions| |pypi-version|

Features
========

* cookies and cookie groups are stored in models for easy management
  through Django admin interface
* support for both opt-in and opt-out cookie consent schemes
* removing declined cookies (or non accepted when opt-in scheme is used)
* logging user actions when they accept and decline various cookies
* easy adding new cookies and seamlessly re-asking for consent for new cookies

You can find the source code and development progress on https://github.com/django-commons/django-cookie-consent/.

User Guide
----------

.. toctree::
   :maxdepth: 2

   quickstart
   concept
   usage
   javascript
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


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. |build-status| image:: https://github.com/django-commons/django-cookie-consent/workflows/Run%20CI/badge.svg
    :alt: Build status
    :target: https://github.com/django-commons/django-cookie-consent/actions?query=workflow%3A%22Run+CI%22

.. |code-quality| image:: https://github.com/django-commons/django-cookie-consent/workflows/Code%20quality%20checks/badge.svg
     :alt: Code quality checks
     :target: https://github.com/django-commons/django-cookie-consent/actions?query=workflow%3A%22Code+quality+checks%22

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. |coverage| image:: https://codecov.io/gh/django-commons/django-cookie-consent/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/django-commons/django-cookie-consent
    :alt: Coverage status

.. |docs| image:: https://readthedocs.org/projects/django-cookie-consent/badge/?version=latest
    :target: https://django-cookie-consent.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. |python-versions| image:: https://img.shields.io/pypi/pyversions/django-cookie-consent.svg

.. |django-versions| image:: https://img.shields.io/pypi/djversions/django-cookie-consent.svg

.. |pypi-version| image:: https://img.shields.io/pypi/v/django-cookie-consent.svg
    :target: https://pypi.org/project/django-cookie-consent/
