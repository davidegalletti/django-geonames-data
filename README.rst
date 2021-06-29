=============================
django-geonames-data
=============================

.. image:: https://badge.fury.io/py/django-geonames-data.svg
    :target: https://badge.fury.io/py/django-geonames-data

.. image:: https://travis-ci.org/davidegalletti/django-geonames-data.svg?branch=master
    :target: https://travis-ci.org/davidegalletti/django-geonames-data

.. image:: https://codecov.io/gh/davidegalletti/django-geonames-data/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/davidegalletti/django-geonames-data

Easy local replica of geonames data by country

Documentation
-------------

The full documentation is at https://django-geonames-data.readthedocs.io.

Quickstart
----------

Install django-geonames-data::

    pip install django-geonames-data

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'geonames.apps.GeonamesConfig',
        ...
    )

Add django-geonames-data's URL patterns:

.. code-block:: python

    from geonames import urls as geonames_urls


    urlpatterns = [
        ...
        url(r'^', include(geonames_urls)),
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
