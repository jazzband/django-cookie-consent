========
Settings
========

``COOKIE_CONSENT_NAME``
  name of consent cookie that remembers user choice

  Default: ``cookie_consent``.

``COOKIE_CONSENT_MAX_AGE``
  max-age of consent cookie

  Default: 1 year

``COOKIE_CONSENT_DECLINE``
  decline value
  Default: ``-1``

``COOKIE_CONSENT_ENABLED``
  boolean or callable that receives request and return boolean.

  IE if you want to enable cookie consent for debug or staff only::

    COOKIE_CONSENT_ENABLED = lambda r: DEBUG or (r.user.is_authenticated() and r.user.is_staff)

  Default: ``True``

``COOKIE_CONSENT_OPT_OUT``
  Boolean value represents if cookies are opt-in or opt-out
  opt-out cookies are set until declined
  opt-in cookies are set only if accepted

  Default: ``False``

``COOKIE_CONSENT_CACHE_BACKEND``
  Alias for backend to use for caching.

  Default: ``default``

``COOKIE_CONSENT_LOG_ENABLED``
  Boolean value representing if logging is turned on or off for when users accept/decline cookies. Turning it off might be useful for preventing your database from getting filled up with log items.

  Default: ``True`` 

``COOKIE_CONSENT_SAMESITE``
  Boolean value representing the samesite attribute for the consent cookie which should be restricted to a first-party or same-site context. 

  Default: ``True`` 

``COOKIE_CONSENT_DOMAIN``
  String value representing the domain attribute for the consent cookie. This value should be the root domain. All subdomains part of the root domain will also have the consent cookie. 

  Default: ``127.0.0.1``

``COOKIE_CONSENT_SECURE``
  Boolean value representing the secure attribute for the consent cookie. A value of True means the cookie will be sent to the server over an encrypted request over HTTPS. 

  Default: ``True``

``COOKIE_CONSENT_HTTPONLY``
  Boolean value representing the httponly attribute for the consent cookie. A value of True causes the consent cookie to be inaccessible to the JavaScript Document.cookoie API and it will instead only be sent to the server which helps against XSS attacks. 

  Default: ``True``

``COOKIE_CONSENT_SIGNED``
  Boolean value representing whether the consent cookie is signed or unsigned. A signed cookie has a signature to detect if the client modified the cookie. 

  Default: ``True``
