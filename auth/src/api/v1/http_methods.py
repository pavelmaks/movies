import aiohttp


def _response(status, **kwargs):
    response = {'status': status}
    response.update(kwargs)
    return response


async def _request(url: str, method: str, **kwargs) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.request(method, url, **kwargs) as response:
            return await response.json()
