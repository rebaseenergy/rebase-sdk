Setting up a site
=================

Create a site
-------------

Following are a few examples of how to use :meth:`rebase.Site.create` to create sites of different kinds.

Common for all sites are that they need a position (latitude, longitude) as well as a name and type.
Full site configuration requirements can be viewed on the :ref:`configurations` page.


Solar
~~~~~

Create a site that will be used to forecast PV power production.

::

  >>> import rebase as rb

  >>> site_config = {
  >>>   'type': 'solar',
  >>>   'name': 'My solar site',
  >>>   'latitude': 53.41,
  >>>   'longitude': 5.94,
  >>>   'azimuth': 171.3, # 0 = North, 90 = East, 180 = South, 270 = West
  >>>   'tilt': 10.3,
  >>>   'capacity': [
  >>>     {'value': 750.5, 'validFrom': '2019-10-10T00:00:00Z'}, # capacity of site changed to 750.5 kW at this date
  >>>     {'value': 500.3, 'validFrom': '2019-04-03T00:00:00Z'}, # site was installed at this date
  >>>   ],
  >>> }

  >>> site_id = rb.Site.create(site_config)


Wind
~~~~

Create a site that will be used to forecast wind power production.

::

  >>> import rebase as rb

  >>> site_config = {
  >>>   'type': 'wind',
  >>>   'name': 'My wind site',
  >>>   'latitude': 53.41,
  >>>   'longitude': 5.94,
  >>>   'capacity': [
  >>>     {'value': 4000, 'validFrom': '2019-10-10T00:00:00Z'}, # capacity of site changed to 4000 kW at this date
  >>>     {'value': 2000, 'validFrom': '2019-04-03T00:00:00Z'}, # site was installed at this date
  >>>   ],
  >>> }

  >>> site_id = rb.Site.create(site_config)


Localized weather
~~~~~~~~~~~~~~~~~

Create a site that will be used to forecast localized weather. Localized weather
is an AI point weather forecast at the site's location, trained on historical data of a certain weather variable.
For example, to get a localized wind speed you will upload historically observed wind speed data.

::

  >>> import rebase as rb

  >>> site_config = {
  >>>   'type': 'localized',
  >>>   'name': 'My localized site',
  >>>   'latitude': 53.41,
  >>>   'longitude': 5.94,
  >>>   'measurement': 'WindSpeed'
  >>> }

  >>> site_id = rb.Site.create(site_config)

Electricity demand
~~~~~~~~~~~~~~~~~~

Create a site that will be used to forecast electricity demand.

::

  >>> import rebase as rb

  >>> site_config = {
  >>>    'type': 'load',
  >>>    'name': 'My load site',
  >>>    'latitude': 53.41,
  >>>    'longitude': 5.94,
  >>>    'nwps': ['DWD_ICON-EU', 'NCEP_GFS'],
  >>>    'variables': [
  >>>        {'name': 'Temperature', 'lag': [-4, -3, -2, -1, 1, 2, 3, 4]},
  >>>        {'name': 'SolarDownwardRadiation'},
  >>>    ],
  >>>    'calendar': ['holidays', 'hourOfDay'],
  >>> }

  >>> site_id = rb.Site.create(site_config)

Get your site(s)
----------------

List all of your sites using :meth:`rebase.Site.list`

::

  >>> import rebase as rb

  >>> sites = rb.Site.list()

Get a single site by its id using :meth:`rebase.Site.get`

::

  >>> import rebase as rb

  >>> site_id = '4ab82692-3944-4069-9cbb-f9c59513c1c3'
  >>> sites = rb.Site.get(site_id)


.. _upload_data:

Upload data to train on
-----------------------
First create a `pandas DataFrame <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html/>`_ with your site's data. The DataFrame needs to contain these exact two columns (all other will be disregarded):

- **valid_time** (datetime, or parseable date strings) - a column containing the data timestamps
- **observation** (numeric) - a column containing the data values

See example DataFrame printed below:

::

  >>> import rebase as rb
  >>> import pandas as pd

  >>> df = pd.read_csv('example_data.csv')
  >>> print(df)
           valid_time                observation
  0        2020-01-22 00:00:00+00:00       126.3
  1        2020-01-22 00:15:00+00:00       122.7
  .        ...                             ...
  n-1      2020-10-17 23:30:00+00:00       169.2
  n        2020-10-17 23:45:00+00:00       176.6

Second, simply upload the data for your site as follows:

::

  >>> site_id = '4ab82692-3944-4069-9cbb-f9c59513c1c3' # replace with your site's id
  >>> rb.Site.upload(site_id, df)


Train a new model for your site
-------------------------------

After uploading observed data for your site, start the training using :meth:`rebase.Site.train`

::

  >>> import rebase as rb

  >>> site_id = '4ab82692-3944-4069-9cbb-f9c59513c1c3' # replace with your site's id
  >>> rb.Site.train(site_id)

Check your site's training status. See :meth:`rebase.Site.status` for more information.

::

  >>> rb.Site.status(site_id)
  {
      'status': 'complete',
      'history': [
          {'state': 'queued', 'timestamp_utc': '2020-10-12 13:04:17'},
          {'state': 'training', 'timestamp_utc': '2020-10-12 13:04:22'},
          {'state': 'complete', 'timestamp_utc': '2020-10-12 13:05:23'},
      ]
  }

.. _get_site_forecast:

Get a site forecast
-------------------

Get your site's latest forecast using :meth:`rebase.Site.forecast`

::

  >>> import rebase as rb

  >>> site_id = '4ab82692-3944-4069-9cbb-f9c59513c1c3' # replace with your site's id
  >>> data = rb.Site.forecast(site_id)
