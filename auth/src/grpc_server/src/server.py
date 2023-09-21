import asyncio
import datetime as dt
import json
import logging
from concurrent.futures import ThreadPoolExecutor

import grpc
import jwt
from api.v1.http_methods import _request
from core.config import settings

import auth_pb2
import auth_pb2_grpc

logging.basicConfig(level=logging.DEBUG)


class GRPC_Service(
    auth_pb2_grpc.AuthServicer
):
    async def is_valid(self, token: str):
        try:
            payload = jwt.decode(token, settings.jwt_key, [settings.ALGORITHM])
            success = all((isinstance(payload, dict), payload.get('exp', 0) > dt.datetime.utcnow().timestamp()))
        except Exception:
            return {'success': False}
        return {'success': success}

    async def CheckerToken(self, request, context):
        """Название метода должно совпадать с названием rpc service в protobuf"""
        if not request.token:
            context.abort(grpc.StatusCode.NOT_FOUND, "token not found")

        payload = await self.is_valid(request.token)
        return auth_pb2.CheckTokenResponse(
            validations=[
                auth_pb2.AuthInfo(is_success=payload['success'])])

    async def LoginAuth(self, request, context):
        """Название метода должно совпадать с названием rpc service в protobuf"""
        if not request.login and request.password:
            context.abort(grpc.StatusCode.NOT_FOUND, "login or password not found")

        response = await _request(f'{settings.AUTH_URL}/api/v1/auth/login',
                                  'post',
                                  data=json.dumps({
                                      "username": request.login,
                                      "password": request.password
                                  }),
                                  headers={'accept': 'application/json',
                                           'Content-Type': 'application/json'})
        return auth_pb2.AuthorizationResponse(tokens=response)


async def serve():
    server = grpc.aio.server(ThreadPoolExecutor(max_workers=10))
    auth_pb2_grpc.add_AuthServicer_to_server(GRPC_Service(), server)

    server.add_insecure_port(f"{settings.GRPC_SERVER_ADDRESS}:{settings.GRPC_SERVER_PORT}")

    await server.start()
    logging.info("grpc server started")
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())
