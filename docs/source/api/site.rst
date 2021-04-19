===========
rebase.Site
===========

Overview
--------

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
-------
.. autoclass:: rebase.Site
   :members:


.. _configurations:

Configurations
--------------

There are currently 4 different supported types of sites:

- :ref:`solar_config`
- :ref:`wind_config`
- :ref:`localized_config`
- :ref:`load_config`

Each of them requires a specific configuration when being created from rb.Site.create(), which you can find below.

.. _solar_config:

Solar
~~~~~

.. list-table:: Required attributes
   :widths: 15 65 20
   :header-rows: 1

   * - Attribute
     - Description
     - type
   * - type
     - Type of site (must be ``solar`` in this case)
     - string
   * - name
     - Name to give your site
     - string
   * - latitude
     - Latitude of your site, ranging from ``29.5`` to ``70.5``
     - float
   * - longitude
     - Longitude of your site, ranging from ``-23.5`` to ``45.0``
     - float
   * - azimuth
     - Orientation of your solar panels,

       ``North = 0, East = 90, South = 180, West = 270`` degrees
     - float
   * - tilt
     - Tilt of your solar panels

       ``0`` to ``90`` degrees
     - float
   * - capacity
     - Capacity of your site. Should be an array containing one object for each capacity change on this format:

       ``[{value: v0, validFrom: d0}, ..., {value: vn, validFrom: dn}]``

       value of ``value`` key must be the capacity in kW as a float

       value of ``validFrom`` key must be an ISO 8601 formatted date string from when the capacity is valid from
     - JSON array of JSON objects

Example:
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
   ],
 }

.. _wind_config:

Wind
~~~~

.. list-table:: Required attributes
   :widths: 15 65 20
   :header-rows: 1

   * - Attribute
     - Description
     - type
   * - type
     - Type of site (must be ``wind`` in this case)
     - string
   * - name
     - Name to give your site
     - string
   * - latitude
     - Latitude of your site, ranging from ``29.5`` to ``70.5``
     - float
   * - longitude
     - Longitude of your site, ranging from ``-23.5`` to ``45.0``
     - float
   * - capacity
     - Capacity of your site. Should be an array containing one object for each capacity change on this format:

       ``[{value: v0, validFrom: d0}, ..., {value: vn, validFrom: dn}]``

       value of ``value`` key must be the capacity in kW as a float

       value of ``validFrom`` key must be an ISO 8601 formatted date string from when the capacity is valid from
     - JSON array of JSON objects

Example:
::

 {
   'type': 'wind',
   'name': 'My wind site',
   'latitude': 53.41,
   'longitude': 5.94,
   'capacity': [
     {'value': 4000, 'validFrom': '2019-10-10T00:00:00Z'}, # capacity of site changed to 4000 kW at this date
     {'value': 2000, 'validFrom': '2019-04-03T00:00:00Z'}, # site was installed at this date
   ],
 }

.. _localized_config:

Localized weather
~~~~~~~~~~~~~~~~~

.. list-table:: Required attributes
   :widths: 15 65 20
   :header-rows: 1

   * - Attribute
     - Description
     - type
   * - type
     - Type of site (must be ``localized`` in this case)
     - string
   * - name
     - Name to give your site
     - string
   * - latitude
     - Latitude of your site, ranging from ``29.5`` to ``70.5``
     - float
   * - longitude
     - Longitude of your site, ranging from ``-23.5`` to ``45.0``
     - float
   * - measurement
     - The type of measurement data to predict

       Must be one of:

       ``WindSpeed / Temperature / CloudCover``
     - string

Example:
::

 {
   'type': 'localized',
   'name': 'My localized site',
   'latitude': 53.41,
   'longitude': 5.94,
   'measurement': 'WindSpeed'
 }

.. _load_config:

Electricity demand
~~~~~~~~~~~~~~~~~~

.. list-table:: Required attributes
   :widths: 15 65 20
   :header-rows: 1

   * - Attribute
     - Description
     - type
   * - type
     - Type of site (must be ``load`` in this case)
     - string
   * - name
     - Name to give your site
     - string
   * - latitude
     - Latitude of your site, ranging from ``29.5`` to ``70.5``
     - float
   * - longitude
     - Longitude of your site, ranging from ``-23.5`` to ``45.0``
     - float
   * - nwps
     - An array of one or more NWPS to train on

       Must be one or more of:

       - ``DWD_ICON-EU``
       - ``NCEP_GFS``
     - JSON array of strings
   * - variables
     - Array of NWP variables and lags to use in training

       Available variables:

       - ``Temperature``
       - ``SolarDownwardRadiation``
       - ``WindSpeed``
       - ``WindDirection``
       - ``CloudCover``

       Each variable can have an optional array of lags with values in range ``-24`` to ``24``


     - JSON array of JSON objects
   * - variables
     - Array of calendar features that should be included in training

       Available features:

       - ``holidays`` - If the model should take public holidays into account
       - ``hourOfDay`` - If the model should take into account which hour of the day it is
       - ``dayOfWeek`` - If the model should take into account which day of the week it is
       - ``weekOfYear`` - If the model should take into account which week of the year it is

     - JSON array of JSON strings


Example:
::

 {
    'type': 'load',
    'name': 'My load site',
    'latitude': 53.41,
    'longitude': 5.94,
    'nwps': ['DWD_ICON-EU', 'NCEP_GFS'],
    'variables': [
        {'name': 'Temperature', 'lag': [-4, -3, -2, -1, 1, 2, 3, 4]},
        {'name': 'SolarDownwardRadiation'},
    ],
    'calendar': ['holidays', 'hourOfDay'],
 }
