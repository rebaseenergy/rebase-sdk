API Reference
=============

Site
----

Overview
~~~~~~~~

.. currentmodule:: rebase.Site

.. autosummary::
  create
  forecast
  get
  delete
  list
  status
  train
  upload


Methods
~~~~~~~
.. autoclass:: rebase.Site
   :members:


.. _configurations:

Configurations
~~~~~~~~~~~~~~~~~~~

There are currently 4 different supported types of sites:

- ``Solar``
- ``Wind``
- ``Localized weather``
- ``Load``

Each of them requires a specific configuration when being created from rb.Site.create(), which you can find below.


``Solar``

::

  {
    'type': 'solar',
    'name': 'My solar site',
    'latitude': 53.41,
    'longitude': 5.94,
    'azimuth': 171.3, # 0 = North, 90 = East, 180 = South, 270 = West
    'tilt': 10.3,
    'capacity': [
      {'value': 750.5, 'validFrom': '2019-10-10T00:00:00Z'}, # capacity of site changed to 750.5 kW at this date
      {'value': 500.3, 'validFrom': '2019-04-03T00:00:00Z'}, # site was installed at this date
    ]
  }

``Wind``

::

  {
    'type': 'wind'
  }

``Localized weather``

::

  {
    'type': 'localized'
  }

``Load``

::

  {
    'type': 'load'
  }
