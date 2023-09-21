import json
from dataclasses import dataclass

import aiohttp


@dataclass
class HTTPResponse:
    body: dict
    status: int


async def aiohttp_client():
    client = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False))
    yield client
    await client.close()

def get_request(aiohttp_client):
    async def inner(url: str, method: str, params: dict = None, headers: dict = {'Content-Type': 'application/json'},
                    token: str = None) -> HTTPResponse:
        if token:
            headers = {**headers, 'Authorization': f'Bearer {token}'}

        params = params or {}

        async with aiohttp_client.get(url, params=params, headers=headers) as response:
            return HTTPResponse(
                body=await response.json(),
                status=response.status,
            )

    return inner


def post_request(aiohttp_client):
    async def inner(url: str, method: str, params: dict = None, headers: dict = {'Content-Type': 'application/json'},
                    token: str = None) -> HTTPResponse:
        if token:
            headers = {**headers, 'Authorization': f'Bearer {token}'}
        params = params or {}

        async with aiohttp_client.post(url, data=json.dumps(params),
                                       headers=headers) as response:
            return HTTPResponse(
                body=await response.json(),
                status=response.status,
            )

    return inner


