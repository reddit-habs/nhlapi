.. _quickstart:

Quick start
===========
This library is very easy to use. First choose your HTTP client. If you are using `asyncio` use
:class:`nhlapi.AsyncClient`, which uses `aiohttp`. If you are using synchronous code or aren't sure what the `asyncio`
module does, use :class:`nhlapi.SyncClient`, which uses the `requests` library.

Depending on which client you choose, you will need to install the HTTP library it depends on.

* For :class:`nhlapi.SyncClient`, :code:`pip install requests`
* For :class:`nhlapi.AsyncClient`, :code:`pip install aiohttp`

Then, create an instance of :class:`nhlapi.endpoints.NHLAPI` passing it client you have selected.

Synchronous::

    api = NHLAPI(nhlapi.SyncClient())
    result = api.teams()

Asynchronous::

    api = NHLAPI(nhlapi.AsyncClient())
    result = await api.teams()

That's pretty much it! You are ready to start using the library.

In order to facilitate working with JSON, this library offers a pretty neat way of accessing items of a dictionary.
See :ref:`props`.

When you are familiar with the attribute access dictionary, check out the :ref:`endpoints` to know how to access the
API.
