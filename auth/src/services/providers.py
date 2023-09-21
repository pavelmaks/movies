from fastapi import Depends
from services.auth import ServiceAuth, get_service_auth
from api.v1.http_methods import _request
from core.config import yandex_settings
from fastapi import HTTPException, Request, status
from services.abstracts import AbstractProvider


class YandexProvider(AbstractProvider):
    async def login(self):
        return {
            'url': yandex_settings.URI.format(yandex_settings.CLIENT_ID, yandex_settings.REDIRECT_URI)
        }

    async def callback(self, request: Request):
        code = request.query_params.get("code")
        if not code:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OAuth authorization failed")
        token_params = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': yandex_settings.CLIENT_ID,
            'client_secret': yandex_settings.CLIENT_SECRET,
            'redirect_uri': yandex_settings.REDIRECT_URI,
        }
        response = await _request(yandex_settings.TOKEN_URI, 'post', data=token_params)
        access_token = response.get('access_token')
        if not access_token:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OAuth authorization failed")
        headers = {'Authorization': f'OAuth {access_token}'}
        info = await _request(yandex_settings.INFO_URI, 'get', headers=headers)

        return await self.service_auth.convert_provider_to_user_tokens('yandex', info.get('id'))


class ProviderDoesNotExist(Exception):
    pass


async def get_provider(provider: str, service_auth: ServiceAuth = Depends(get_service_auth)):
    if provider == 'yandex':
        return YandexProvider(service_auth)
    else:
        raise ProviderDoesNotExist()
