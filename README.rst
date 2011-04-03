django-cachebuster -- A backwards-compatible Django 1.3+ ready set of cache-busting template tags
=================================================================================================


Overview
--------

**django-cachebuster** is a Django app containing two template tags: ``static`` and ``media``.  Each tag will use the file last modified timestamp by default to 'bust' web browser file caches.  ``static`` is meant for your site's JavaScript, CSS and standard images.  ``media`` is intended for user uploaded content like avatars, videos and other files.  CloudFront and other content delivery networks are supported.


Description
-----------

All of the existing file cache busting techniques seem to be Django versions 1.2.x and lower oriented - meaning they don't support the new ``django.contrib.staticfiles`` paradigm.  This app addresses this functionality gap.

Additionally, there are some optimizations (see **Configuration** below) that can be enabled to minimize file modification date disk reads.


Requirements
------------

- Python 2.6 (May work with prior versions, but untested - please report)
- Django 1.2.x, 1.3.x (May work with prior versions, but untested - please report)


Installation
------------

Copy or symlink the 'cachebuster' package into your django project directory or install it by running one of the following commands:

::

    python setup.py install

::

    pip install django-cachebuster

::

    easy_install django-cachebuster

Now, add ``cachebuster`` to your ``INSTALLED_APPS`` in your project's ``settings.py`` module.


Template Usage
----------------------

To use these cache-busting template tags, you'll need to load the template tag module at the top of each template with ``{% load cachebuster %}``.  Alternatively, as these tags will most likely be used in most of a project's templates, you can tell Django to auto-load them without the requisite ``{% load cachebuster %}`` by adding the following to your ``settings.py``:

::

    from django.template.loader import add_to_builtins
    add_to_builtins('cachebuster.templatetags.cachebuster')

``{% static filename %}`` attempts to use the ``CACHEBUSTER_UNIQUE_STRING`` (see **Configuration** below) setting to get a cached value to append to your static URLs (ie. ``STATIC_URL``).  If ``CACHEBUSTER_UNIQUE_STRING`` is not set, it falls back to the last date modified of the file.  If ``CACHEBUSTER_UNIQUE_STRING`` is used, you can force last-date-modified behaviour by adding ``True`` into the tag statement like so: ``{% static filename True %}``.  For example

::

    <link rel="stylesheet" href="{% static css/reset.css %}" type="text/css">
    <link rel="stylesheet" href="{% static css/fonts.css True %}" type="text/css">

This would yield something along the lines of:

::

    <link rel="stylesheet" href="/static/css/reset.css?927f6b650afce4111514" type="text/css">
    <link rel="stylesheet" href="/static/css/fonts.css?015509150311" type="text/css">

``{% media filename %}`` is similar but has slightly different behaviour, as the file content has a different origin (user uploaded content like avatars, videos, etc.) and cannot depend on any git comment hash.  This is why there is no behaviour other than the last modified date method for MEDIA_URL files.

::

    <img src='{% media uploads/uid1-avatar.jpg %}' />

would result in something like this:

::

    <img src='/media/uploads/uid1-avatar.jpg?034511190510' />


Configuration
--------------------

**django-cachebuster** supports two methods of 'busting'.  Appending a unique string (by default, this is the last modified datetime of the file) as a query string parameter is the easy, default behaviour.  For more advanced requirements such as content distribution network (CDN, such as CloudFront) scenarios, there is also the ability to prepend the unique string.

To start using it in it's simplest form right now, see the **Template Usage** section.  Want more from **django-cachebuster**?  Read on.

``CACHEBUSTER_UNIQUE_STRING``: **optional**; defaults to the file's last modified timestamp.

This is a simple performance optimization that minimizes accessing the file system to get a file's last modified timestamp.  This optimization is only used for static files (not media/user-generated files) as only static files are usually version-controlled.

To set ``CACHEBUSTER_UNIQUE_STRING``, you would mostly likely use a provided 'detector' or write your own (please contribute new ones!).  For example, if you use Git as your source control, you can use the provided ``git`` detector.  It simply traverses the Django project's path looking for the ``.git`` folder, and then extracts the current commit hash.  This hash is cached and used for subsequent cache-busting.  In your settings.py:

::

    from cachebuster.detectors import git
    CACHEBUSTER_UNIQUE_STRING = git.unique_string(__file__)

or if you wanted it to be a short busting string:

::

    from cachebuster.detectors import git
    CACHEBUSTER_UNIQUE_STRING = git.unique_string(__file__)[:8]

``__file__`` must be passed in so that **django-cachebuster** operates in the context of the Django project's settings.py file.  If it wasn't passed in, django-cachebuster would only have its own context from which to grab the ``.git`` directory, not that of the user's project.  (An alternative to this is to use Python's ``inspect`` module - but there are some warnings around using it.)

``CACHEBUSTER_PREPEND_STATIC``: **optional**; defaults to ``False``.

``CACHEBUSTER_PREPEND_MEDIA``: **optional**; defaults to ``False``.

If CloudFront or another CDN that ignores query string parameters is used, ``CACHEBUSTER_PREPEND_STATIC`` will need to be set to ``True``.  For static files, this prepends the unique string instead of appending it as a query string parameter.  ``CACHEBUSTER_PREPEND_MEDIA`` does the same for media files.  For example, with ``CACHEBUSTER_PREPEND_STATIC`` set to True, the rendered output becomes:

::

    <link rel="stylesheet" href="/static/927f6b650afce4111514/css/reset.css" type="text/css">

With ``CACHEBUSTER_PREPEND_STATIC`` set to False:

::

    <link rel="stylesheet" href="/static/css/reset.css?927f6b650afce4111514" type="text/css">

Using this prepending method raises a couple of development environment issues, however.  Assuming Django 1.3 or higher is used, ``./manage.py runserver`` will automatically attempt to serve static (not media, however) files on its own without any urls.py changes; this standard method of serving does not work in this scenario.  To prevent this default Django behaviour, the development server should be started with the following command:

::

    ./manage.py runserver --nostatic

Also when using the prepending method in a development environment, to support serving files from both ``{% static %}`` and ``{{ STATIC_URL }}`` (as well as ``{% media %} and ``{{ MEDIA_URL }}``), Django's default ``serve`` views need to be replaced with the following in your ``urls.py``:

::

    if settings.DEBUG:
        urlpatterns += patterns('',
            url(r'^static/(?P<path>.*)$', 'cachebuster.views.static_serve', {'document_root': settings.STATIC_ROOT,}),
            url(r'^media/(?P<path>.*)$', 'cachebuster.views.media_serve', {'document_root': settings.MEDIA_ROOT,}),
        )

This is because both the prepended and the non-prepended paths need to be tested to support the above-mentioned scenarios.


Troubleshooting
----------------------

**My date-based cache-busting unique strings keep updating even though my assets aren't changing**

Are you deploying your assets from a source control system such as Subversion or Git?  By default, those systems set the last modified date of checked-out files to their check-out dates, **not** the original files' last modified dates. To fix this on Subversion, set ``use-commit-times=true`` in your Subversion config. In Git this is a little harder; it requires adding a Git post-checkout hook (or updating your deployment script). For more instructions on doing this, see the answers to `this question on Stack Overflow <http://stackoverflow.com/questions/1964470/whats-the-equivalent-of-use-commit-times-for-git>`_.


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