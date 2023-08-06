from __future__ import annotations

import logging, asyncio

from typing import Any, Optional, Set

from aiohttp import web
from aiohttp.web import Request
from discord import Client, utils
from rich.logging import RichHandler
from logging import getLogger
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from json import loads, dumps

log = getLogger("REST")


__all__ = ("RestClient",)


class RestClient:
    def __init__(
        self,
        client: Client,
        *,
        route: str = "/interactions",
        app: Optional[web.Application] = None,
    ):
        self._client = client
        self._app = app or web.Application()
        self._route = route
        self._verify_key: VerifyKey = utils.MISSING
        self._app.add_routes([web.post(self._route, self.handle_interactions)])

    def get_latest_task(
        self, before_tasks: Set[asyncio.Task[Any]]
    ) -> asyncio.Task[None]:
        return (asyncio.all_tasks() - before_tasks).pop()

    async def verify_request(self, request: Request):
        signature = request.headers.get("X-Signature-Ed25519")
        timestamp = request.headers.get("X-Signature-Timestamp")

        if not signature or not timestamp:
            return False
        try:
            self._verify_key.verify(
                f"{timestamp}{await request.text()}".encode(), bytes.fromhex(signature)
            )
        except BadSignatureError as e:
            return False

        return True

    async def handle_interactions(self, request: Request):
        if not await self.verify_request(request):
            response = await utils.maybe_coroutine(lambda r: None, request)
            return web.Response(status=401, body=response)

        data = loads(await request.text())
        if data["type"] == 1:
            return web.Response(body=dumps({"type": 1}))

        tasks = asyncio.all_tasks()
        self._client._connection.parse_interaction_create(data)
        if len(tasks):
            await self.get_latest_task(tasks)
        response = await utils.maybe_coroutine(lambda r: None, request)
        return web.Response(status=200, body=response)

    async def start(self, token: str, **kwargs):
        kwargs["print"] = None
        utils.setup_logging(
            handler=RichHandler(show_time=kwargs.get("show_time", False))
        )
        await self._client.login(token)

        assert self._client.application is not None
        self._verify_key = VerifyKey(bytes.fromhex(self._client.application.verify_key))
        log.info(
            f"Running on https://{kwargs.get('host', 'localhost')}:{kwargs.get('port', 8080)}{self._route}"
        )
        self._client.dispatch("ready")
        await web._run_app(self._app, **kwargs)
