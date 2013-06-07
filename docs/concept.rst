=============
Main concepts
=============

Cookie Group
------------

Cookie Group model represents a group of related cookies. For all but
required cookie groups, user gives consent or decline their use.

Versions
^^^^^^^^

Each Cookie Group has current version that is timestamp when last cookie
is added. When user accept cookie group, current version is saved in
``cookie_consent`` cookie.

Versions allows django-cookie-consent app
to know if new cookies have been introduced since user given a consent for
specific cookie use and to ask them to re-accept new cookies when needed.

Important attributes:
^^^^^^^^^^^^^^^^^^^^^

``varname``
  Variable name that will be used for this cookie group.

``is_required``
  Required cookies are not deleted and user cannot affect them.
  This could be ``sessionid``, ``csrftoken`` and others.
  Without this cookies website will not work properly and user can't opt-out.

``is_deletable``
  If cookie group is deletable, django-cookie-consent will try
  to delete cookies in this group when declined or through
  ``CleanCookiesMiddleware`` middleware.


Cookie
------

Cookie model represent each cookie.
Note that ``domain`` and ``path`` attributes are important for deleting
cookies.

Saving user selection
---------------------

User selection regard cookie use are saved in a cookie with default name
``cookie_consent``.

Example of ``cookie_consent`` value could be::

    optional=-1|social=2013-06-04T03:17:01.421395

In above example user declined cookie group with ``optional`` varname
and accepted cookie group ``social`` with all cookies created before
stated timestamp.

Caching
-------

To avoid hitting database for each request, non required
cookies and cookie groups are cached.
