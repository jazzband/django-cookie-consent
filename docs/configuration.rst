=============
Configuration
=============

1. Add ``cookie_consent`` to your ``INSTALLED_APPS``.

2. Add ``django.template.context_processors.request``
   to ``TEMPLATE_CONTEXT_PROCESSORS`` if it is not already added.

3. Include django-cookie-consent urls in ``urls.py``

    .. code-block:: python

        from django.urls import path

        urlpatterns = [
            ...,
            path("cookies/", include("cookie_consent.urls")),
            ...,
        ]

4. Run the ``migrate`` management command to update your database tables:

    .. code-block:: bash

        python manage.py migrate
