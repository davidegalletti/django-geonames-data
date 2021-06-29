=====
Usage
=====

To use django-geonames-data in a project, add it to your `INSTALLED_APPS`:

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
