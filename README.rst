=============================
Plugs Store
=============================

.. image:: https://badge.fury.io/py/plugs-store.svg
    :target: https://badge.fury.io/py/plugs-store

.. image:: https://travis-ci.org/beatrizseabra/plugs-store.svg?branch=master
    :target: https://travis-ci.org/beatrizseabra/plugs-store

.. image:: https://codecov.io/gh/beatrizseabra/plugs-store/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/beatrizseabra/plugs-store

Pluggable Store

Documentation
-------------

The full documentation is at https://plugs-store.readthedocs.io.

Quickstart
----------

Install Plugs Store::

    pip install plugs-store

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'plugs_store.apps.PlugsStoreConfig',
        ...
    )

Add Plugs Store's URL patterns:

.. code-block:: python

    from plugs_store import urls as plugs_store_urls


    urlpatterns = [
        ...
        url(r'^', include(plugs_store_urls)),
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

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
