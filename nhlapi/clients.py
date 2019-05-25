from .props import wrap

try:
    import requests

    class SyncClient:
        def __init__(self, headers=None):
            self._sess = requests.Session()
            if headers:
                self._sess.headers.update(headers)

        def get(self, url, params=None):
            resp = self._sess.get(url, params=params)
            resp.raise_for_status()
            return wrap(resp.json())


except ImportError:
    pass


try:
    import aiohttp
    import asyncio

    class AsyncClient:
        def __init__(self, *, headers=None, loop=None):
            if not loop:
                loop = asyncio.get_event_loop()
            self._loop = loop
            self._session = aiohttp.ClientSession(headers=headers, loop=self._loop)

        def __del__(self):
            asyncio.ensure_future(self._session.close(), loop=self._loop)

        async def get(self, url, params=None):
            resp = await self._session.get(url, params=params)
            resp.raise_for_status()
            return wrap(await resp.json())


except ImportError:
    pass
