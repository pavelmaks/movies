import grpc
from core.config import settings
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .grpc_client import auth_pb2
from .grpc_client.auth_pb2_grpc import AuthStub

security = HTTPBearer()


class HasAccess:
    def __init__(self, roles: list[str]):
        self.roles = roles

    async def __call__(self, credentials: HTTPAuthorizationCredentials = Depends(security)):
        async with grpc.aio.insecure_channel(f'{settings.grpc_server_address}:{settings.grpc_server_port}') as channel:
            client = AuthStub(channel)
            request = auth_pb2.CheckTokenRequest(token=credentials.credentials)
            response = await client.CheckerToken(request)
            if response.validations[0].is_success:
                return True

        raise HTTPException(status_code=401, detail='Для просмотра необходимо произвести вход по адресу /login')


all_access = HasAccess([])
admin_access = HasAccess(['admin'])
