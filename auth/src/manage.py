import argparse
import asyncio
import logging
from getpass import getpass

from api.v1.exception import UserCreateException
from api.v1.schemas.auth import SingUpForm
from db.models.role import Role
from db.pg import get_session
from services.role import ServiceRole
from services.user import ServiceUser

logger = logging.getLogger('manage')
logger.addHandler(logging.NullHandler())


def synchronize_async_helper(to_await):
    async_response = []

    async def run_and_capture_result():
        r = await to_await
        async_response.append(r)

    loop = asyncio.get_event_loop()
    coroutine = run_and_capture_result()
    loop.run_until_complete(coroutine)
    return async_response[0]


async def main():
    parser = argparse.ArgumentParser(description='Модуль управления')
    parser.add_argument('createsuperuser', help='Создание суперпользователя', nargs='*')
    args = parser.parse_args()

    if args.createsuperuser:
        db_session = await anext(get_session())

        login = input('Введите логин суперпользователя: ')
        password = getpass(prompt='Введите пароль суперпользователя: ')
        first_name = input('Введите имя: ')
        last_name = input('Введите фамилию: ')

        form = SingUpForm(
            username=login,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        try:
            user = await ServiceUser(db_session).create(form)
            admin_roles = await ServiceRole(db_session).get_roles('admin', 1, 0)
            if admin_roles:
                admin_role: Role = admin_roles.pop()
            await ServiceUser(db_session).add_role(user.id, admin_role.id)
            logger.info('Пользователь с аминистративными привилениями успешно создан')
        except UserCreateException as ex:
            logger.error(ex)


if __name__ == '__main__':
    synchronize_async_helper(main())
