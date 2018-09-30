import asyncio

import aiohttp

from .props import wrap


class Client:
    def __init__(self, *, headers=None, loop=None):
        if not loop:
            loop = asyncio.get_event_loop()
        self._loop = loop
        self._session = aiohttp.ClientSession(headers=headers, loop=self._loop)

    def __del__(self):
        asyncio.ensure_future(self._session.close(), loop=self._loop)

    async def get(self, url, params=None):
        resp = await self._session.get(url, params=params, raise_for_status=True)
        dict = await resp.json()
        return wrap(dict)
