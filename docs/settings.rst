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
  Boolean value represents if user actions when they accepting and declining cookies will be logged. Turning it off might be useful for preventing your database from getting filled up with log items.

  Default: ``True`` 
