=========
Changelog
=========

0.4.0 (in development)
----------------------

.. note:: These release notes are incomplete!

.. note:: The 0.4.0 release has had a project management overhaul. There are no
   functional changes (yet) to the project, but things *around the project* have changed.
   Please check the release notes carefully.


**Breaking changes**

* Dropped support for Django 2.2, 3.0 and 3.1
* Dropped support for Python 3.6

These versions are end-of-life and no longer supported by their upstream teams.

**Bugfixes**

* Cache instance resolution is now lazy (#41)
* Fixed support for Django 4.1 (#73) - thanks @alahdal

**Project maintenance**

* Transferred project to Jazzband (#38, #64, #75)
* Replaced Travis CI with Github Actions (#64, #75)
* Set up correct test matrix for python/django versions (#75)
* Code is now ``isort`` and ``black`` formatted (#75)
* Set up ``tox`` and ``pytest`` for testing (#64, #75)
* 'Removed' the example app - the ``testapp`` in the repository is still a good example

**Documentation**

Did some initial restructuring to make the docs easier to digest, more to come.

0.3.1 (2022-02-17)
------------------

- Protect against open redirect after accepting cookies (#48)


0.3.0 (2021-12-08)
------------------

* support ranges from django 2.2 to 4.0 and python 3.6 to 3.9


0.2.6 (2020-06-17)
------------------

* fix: setup for python 2.7


0.2.5 (2020-06-17)
------------------

* chore: add package descriptions


0.2.4 (2020-06-17)
------------------

* Cookie Bar Choosing Decline Not Disappearing Right Away (#22)

* 📦 NEW: pt_BR (#23)

0.2.3 (2020-06-15)
------------------

* Update package classifiers


0.2.2 (2020-06-15)
------------------

* 8732949 Remove jquery (#20)


0.2.1 (2020-06-02)
------------------

* fix: Set max version for django-appconf (#18)

* fix: Views ignore 'next' url parameter (#12)

* Update configuration.rst


0.2.0 (2020-02-11)
------------------

* support ranges from django 1.9 to 3.0 and python 2.7 to 3.7 (JonHerr)

0.1.1
-----

* tweak admin

* Add accepted_cookies template filter

* Add varname property to Cookie model

* Add translation catalog

0.1.0
-----

* Initial release
