import grpc

from jose import jwt
from jose.exceptions import JOSEError
from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser

from grpc_client.auth_pb2_grpc import AuthStub
from grpc_client import auth_pb2

User = get_user_model()


class CustomBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        if username is None or password is None:
            return
        payload = {'username': username, 'password': password}
        access_token = self.get_token_from_auth_service(payload)
        if access_token:
            user = self.get_or_create_user(access_token)
        else:
            user = self.get_user_from_django(payload)
        return user

    def get_token_from_auth_service(self, payload: dict) -> str | None:
        try:
            response = self.login_grpc(payload['username'], payload['password'])
        except grpc.RpcError:
            return None
        data = response.tokens
        return data['access_token']

    def get_or_create_user(self, token: str) -> AbstractBaseUser | None:
        try:
            data = jwt.decode(token, settings.JWT_KEY, settings.JWT_ALGORITHM)
            user = User.objects.get(user_name=data['user'],)
        except JOSEError:
            return None
        except User.DoesNotExist:
            user = User.objects.create_user(user_name=data['user'])
        user.is_admin = data.get('roles') == ['admin']
        user.save()
        return user

    def get_user_from_django(self, payload: dict) -> AbstractBaseUser | None:
        try:
            user = User.objects.get(user_name=payload['username'],)
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(payload['password']):
                return user

    def login_grpc(self, login: str, password: str):
        with grpc.insecure_channel(settings.GRPC_SERVER_URL) as channel:
            client = AuthStub(channel)
            request = auth_pb2.AuthorizationRequest(login=login, password=password)
            response = client.LoginAuth(request)
            return response

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
