=====
Usage
=====

Checking for cookie consent in views
------------------------------------

.. code-block:: python

  from cookie_consent.util import get_cookie_value_from_request

  def myview(request, *args, **kwargs):
    cc = get_cookie_value_from_request(request, "mycookies")
    if cc:
      # add cookie

Checking if specific cookie in Cookie group is accepted is possible:

.. code-block:: python

    cc = get_cookie_value_from_request(request, "mycookies", "mycookie1")

Checking for cookie consent in templates
----------------------------------------

Use ``cookie_group_accepted`` or ``cookie_group_declined`` template filters.

.. code-block:: django

  {% load cookie_consent_tags %}
  {% if request|cookie_group_accepted:"analytics" %}
    {# load 3rd party analytics #}
  {% endif %}

Bot filters takes cookie group ``varname`` and optional cookie name with
domain. If cookie name with domain is used, format is 
``VARNAME=COOKIENAME:DOMAIN``.


Checking for 3rd party cookies dynamically
------------------------------------------

.. warning::

    .. deprecated:: 0.5.0

    This approach does not work well with page-level caches and (strict) content
    security policies. Instead, use the new :ref:`Javascript <javascript>` approach
    with ``<template>`` nodes.

Using ``js_type_for_cookie_consent`` templatetag for script type attribute
would set ``x/cookie_consent`` thus making browser skip executing this block
of javascript code.

When consent for using specific cookies is given, code can be evaluated
without reloading page.

.. code-block:: django

  {% load cookie_consent_tags %}
  <script type="{% js_type_for_cookie_consent request "social" "*:.google.com" %}" data-varname="social">
    alert("Social cookie accepted");
  </script>


Asking users for cookie consent in templates
--------------------------------------------

.. warning::

   The instructions below refer to the legacy integration. See :ref:`javascript` for
   an updated approach.

   .. deprecated:: 0.5.0

   The legacy integration is deprecated and will be removed in django-cookie-consent
   1.0.0.

``django-cookie-consent`` can show website visitors a cookie consent message. This
message informs users that the website uses cookies and requests their consent
to store them. The script responsible for displaying the message is
``cookiebar.js``. You can see an example of its usage in the testapp.
 
In order to display the cookie consent message on your website:

1. Load the ``cookiebar.js`` script in your HTML template. You can do this by
   adding the following line to the ``<head>`` section of your template:

   .. code-block:: html

      <script type="text/javascript" src="{% static 'cookie_consent/cookiebar.js' %}"></script>

   This script assigns ``window.legacyShowCookieBar`` and the alias ``showCookieBar`` (
   the latter is for backwards compatibility).
  
2. In your JavaScript code, call the ``legacyShowCookieBar`` function with the
   appropriate options object:

.. code-block:: javascript

  window.legacyShowCookieBar({
    content: 'your-cookie-bar-html',
    cookie_groups: ['your-cookie-group'],
    cookie_decline: 'your-decline-cookie-setting',
    beforeDeclined: function () {
    // your code to run before the user declines
    },
  });

Options
=======

The ``legacyShowCookieBar`` function accepts an options object with the following
properties:

* ``content`` (required): A string containing the HTML for your cookie consent
    message.
* ``cookie_groups`` (optional): An array of strings representing the cookie
    consent groups. The script will only execute the scripts associated with
    these groups when the user accepts cookies.
* ``cookie_decline`` (optional): A string representing the cookie value to be set
    when the user declines cookies.
* ``beforeDeclined`` (optional): A callback function that runs before the user
    declines cookies. If you don't want to run any callbacks, set this to
    ``null``.

Example
=======

Here's an example of how to use the legacyShowCookieBar function:

.. code-block:: javascript

  legacyShowCookieBar({
    content: '<div class="cookie-bar"> <p>We use cookies to improve your browsing experience. By continuing to use our site, you agree to our use of cookies.</p> <a href="/accept_cookies" class="cc-cookie-accept">Accept</a> <a href="/decline_cookies" class="cc-cookie-decline">Decline</a> </div>',
    cookie_groups: ['analytics'],
    cookie_decline: '{% get_decline_cookie_groups_cookie_string request analytics %}',
    beforeDeclined: function () {
      console.log('User is about to decline cookies');
    },
  });

One thing to keep in mind is that the legacyShowCookieBar function only adds the HTML
template for the banner to your page - you still need to style it with CSS to
make it work properly.

Notes
=====

* Ensure that the elements with the class names ``cc-cookie-accept`` and
  ``cc-cookie-decline`` are present within the content HTML string.
