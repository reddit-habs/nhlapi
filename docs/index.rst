.. _index:

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

The objects returned by the various endpoints support a syntax similar to JavaScript objects and can be accessed with
the dot notation. See :ref:`props` for more information.

Table of contents
-----------------

.. toctree::
    :numbered:
    :caption: Contents:

    install
    quickstart
    props
    endpoints
    utils
    clients
