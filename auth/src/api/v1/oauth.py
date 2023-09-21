from fastapi import APIRouter, Depends, HTTPException, Request, status
from services.providers import ProviderDoesNotExist, get_provider

router = APIRouter()


@router.get('/{provider}/login',
            summary="Авторизация через социальную сеть",
            description="Авторизация через социальную сеть")
async def login(provider: callable = Depends(get_provider)):
    try:
        return await provider.login()
    except ProviderDoesNotExist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Social provider does not exist")

@router.get('/{provider}/callback',
            summary="Получение токена",
            description="Метод принимает код, который возвращает авторизованный пользователь и получает токен доступа")
async def callback(request: Request, provider: callable = Depends(get_provider)):
    try:
        return await provider.callback(request)
    except ProviderDoesNotExist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Social provider does not exist")
