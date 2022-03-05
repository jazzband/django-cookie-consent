==========
Middleware
==========

CleanCookiesMiddleware
----------------------

.. autoclass:: cookie_consent.middleware.CleanCookiesMiddleware
   :members:

::

    MIDDLEWARE = [
        'cookie_consent.middleware.CleanCookiesMiddleware',
    ]

This middleware will automatically delete previously accepted third party cookies when they are declined or not accepted/declined. 

To test it, try accepting third party cookies on your site until your browser stores those third party cookies. 

Your database values for cookie name, path, and domain must match the third party cookie values that are stored in your browser.

Try declining the previously accepted cookie group or try deleting the COOKIE_CONSENT_NAME cookie from your browser and you will notice in your browser inspect tool that the third party cookies that were accepted for that cookie group are now automatically deleted from the browser. 
