.. nhlapi documentation master file, created by
   sphinx-quickstart on Fri Sep 28 23:36:51 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to nhlapi's documentation!
==================================
This documentation is for the programmatic Python API. It supports both synchronous and asynchronous HTTP clients.
It also offers a few objects that make it easier to interact with the API, such as :class:`nhlapi.utils.Season`.

To get complete information about the NHL API consult `dword4's docs`_.

.. _dword4's docs: https://gitlab.com/dword4/nhlapi/blob/master/stats-api.md

What does this library do?
--------------------------
This library makes endpoints of the NHL API available as methods. They can be called easily with idiomatic objects,
such a :class:`datetime.date` and custom made objects like :class:`nhlapi.utils.Season` and :class:`nhlapi.utils.GameId`.
So for instance, you can easily get the schedule for a specific date using::

    api.schedule(date=datetime.date(2018, 10, 03))

The library also supports synchronous (using `requests`) and asynchronous (using `aiohttp`) HTTP requests transparently.

The objects returned by the various endpoints are *magic* immutable dictionaries that allow access of fields using
properties. So instead of doing::

    data["team"]["name"]

You can do::

    data.team.name

Note that it's still possible to use the square bracket syntax with the *magic* dictionaries.

Getting started
---------------
This library is very easy to use. Create an instance of :class:`nhlapi.endpoints.NHLAPI` with either
:class:`nhlapi.io.Client` or :class:`nhlapi.aio.Client` and start calling endpoints. Note that when using the asynchronous
client, you need to await the calls to endpoints because it returns a future.

Synchronous::

    api = NHLAPI(nhlapi.io.Client())
    result = api.teams()

Asynchronous::

    api = NHLAPI(nhlapi.aio.Client())
    result = await api.teams()

Consult :ref:`endpoints` to know how to access more information.

Table of contents
-----------------

.. toctree::
    :maxdepth: 2
    :numbered:
    :caption: Contents:

    endpoints
    api
