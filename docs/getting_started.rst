===============
Getting started
===============

Checking for cookie consent in views
------------------------------------

::

  from cookie_consent.util import get_cookie_value_from_request

  def myview(request, *args, **kwargs):
    cc = get_cookie_value_from_request(request, "mycookies")
    if cc:
      # add cookie

Checking if specific cookie in Cookie group is accepted is possible::

    cc = get_cookie_value_from_request(request, "mycookies", "mycookie1")

Checking for cookie consent in templates
----------------------------------------

Use ``cookie_group_accepted`` or ``cookie_group_declined`` template filters.

::

  {% load cookie_consent_tags %}
  {% if request|cookie_group_accepted:"analytics" %}
    {# load 3rd party analytics %}
  {% endif %}

Bot filters takes cookie group ``varname`` and optional cookie name with
domain. If cookie name with domain is used, format is 
``VARNAME=COOKIENAME:DOMAIN``.


Checking for 3rd party cookies dynamically
------------------------------------------

Using ``js_type_for_cookie_consent`` templatetag for script type attribute
would set ``x/cookie_consent`` thus making browser skip executing this block
of javascript code.

When consent for using specific cookies is given, code can be evaluated
without reloading page.

::

  {% load cookie_consent_tags %}
  <script type="{% js_type_for_cookie_consent request "social" "*:.google.com" %}" data-varname="social">
    alert("Social cookie accepted");
  </script>
