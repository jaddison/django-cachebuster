django-cachebuster -- A backwards-compatible Django 1.3+ ready set of cache-busting template tags
=================================================================================================


Overview
--------

django-cachebuster is a Django app containing two template tags: ``static`` and ``media``.  Each tag will use the file last modified timestamp by default to 'bust' web browser file caches.  ``static`` is meant for your site's JavaScript, CSS and standard images.  ``media`` is intended for user uploaded content like avatars, videos and other files.


Description
-----------

All of the existing file cache busting techniques seem to be Django versions 1.2.x and lower oriented - meaning they don't support the new ``django.contrib.staticfiles`` paradigm.  This app addresses this functionality gap.

Additionally, there are some optimizations (see Advanced Settings below) that can be enabled to minimize file modification date disk reads.


Requirements
------------

- Python 2.6 (May work with prior versions, but untested - please report)
- Django 1.2.x, 1.3.x (May work with prior versions, but untested - please report)


Installation
------------

Copy or symlink the ``cachebuster`` package into your django project directory or install it by running one of the following commands:

::

    python setup.py install

::

    pip install django-cachebuster

::

    easy_install django-cachebuster

Now, add ``cachebuster`` to your ``INSTALLED_APPS`` in your project's ``settings.py`` module.


Template Usage
----------------------

``{% static filename %}`` attempts to use the ``CACHEBUSTER_UNIQUE_STRING`` (see Advanced Settings below) setting to get a cached value to append to your static URLs (ie. STATIC_URL).  If ``CACHEBUSTER_UNIQUE_STRING`` is not set, it falls back to the last date modified of the file.  If ``CACHEBUSTER_UNIQUE_STRING`` is used, you can force last-date-modified behavior by adding ``True`` into the tag statement like so: ``{% static filename True %}``.  For example

::

    <link rel="stylesheet" href="{% static css/reset.css %}" type="text/css">
    <link rel="stylesheet" href="{% static css/fonts.css True %}" type="text/css">

This would yield something along the lines of:

::

    <link rel="stylesheet" href="/static/css/reset.css?927f6b650afce4111514" type="text/css">
    <link rel="stylesheet" href="/static/css/fonts.css?015509150311" type="text/css">

``{% media filename %}`` is similar but has slightly different behavior, as the file content has a different origin (user uploaded content like avatars, videos, etc.) and cannot depend on any git comment hash.  This is why there is no behaviour other than the last modified date method for MEDIA_URL files.

::

    <img src='{% media uploads/uid1-avatar.jpg %}' />

would result in something like this:

::

    <img src='/media/uploads/uid1-avatar.jpg?034511190510' />

Advanced Settings
----------------------

``CACHEBUSTER_UNIQUE_STRING``: **optional**; no default.

If ``CACHEBUSTER_UNIQUE_STRING`` is not set, the file's last modified datetime will be used for cache-busting.  To set it, you would mostly likely use a ``cachebuster detector``; at the moment, there is a single **detector** available for ``git``.  It simply traverses the project's path looking for the ``.git`` folder, and then extracts the current commit hash.  The hash is cached and used for subsequent cache-busting.  For example, in your settings.py:

::

    from cachebuster.detectors import git
    CACHEBUSTER_UNIQUE_STRING = git.unique_string(__file__)

or if you wanted it to be a short busting string:

::

    from cachebuster.detectors import git
    CACHEBUSTER_UNIQUE_STRING = git.unique_string(__file__)[:8]

``git.unique_string(__file__)`` requires that the user pass in ``__file__`` so that it has the context of your Django settings.py file.  If it wasn't passed in, django-cachebuster would only have its own context from which to grab the ``.git`` directory, not that of the user's project.  (An alternative to this is to use Python's ``inspect`` module - but there are some warnings around using it.)

Notes
-----

Please feel free to send a pull request with fixes and in particular, additional ``detectors`` to improve the usefulness of this app.  Maybe for ``svn``, ``hg``, etc?


Source
------

The latest source code can always be found here: `github.com/jaddison/django-cachebuster <http://github.com/jaddison/django-cachebuster/>`_


Credits
-------

django-cachebuster is maintained by `James Addison <mailto:code@scottisheyes.com>`_.


License
-------

django-cachebuster is Copyright (c) 2011, James Addison. It is free software, and may be redistributed under the terms specified in the LICENSE file.


Questions, Comments, Concerns:
------------------------------

Feel free to open an issue here: `github.com/jaddison/django-cachebuster/issues <http://github.com/jaddison/django-cachebuster/issues/>`_