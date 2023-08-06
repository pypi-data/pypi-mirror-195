=============================
Django Lens
=============================

.. image:: https://badge.fury.io/py/django-lens.svg
    :target: https://badge.fury.io/py/django-lens

.. image:: https://travis-ci.org/v1k45/django-lens.svg?branch=master
    :target: https://travis-ci.org/v1k45/django-lens

.. image:: https://codecov.io/gh/v1k45/django-lens/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/v1k45/django-lens

Enhance your Django development experience

Documentation
-------------

The full documentation is at https://django-lens.readthedocs.io.

Quickstart
----------

Install Django Lens::

    pip install django-lens

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'lens.apps.LensConfig',
        ...
    )

Add Django Lens's URL patterns:

.. code-block:: python

    from lens import urls as lens_urls


    urlpatterns = [
        ...
        url(r'^', include(lens_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox


Development commands
---------------------

::

    pip install -r requirements_dev.txt
    invoke -l


Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
