from core.config import db_settings, settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

dsn = f'postgresql+asyncpg://{db_settings.user}:{db_settings.password}@{db_settings.host}/{db_settings.dbname}'
# точка входа sqlalchemy в приложение
engine = create_async_engine(dsn, echo=settings.DEBUG_ENGINE, future=True)
# создаем сессии чтобы можно было работать с бд
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    """Получение асинхронной сессии"""
    async with async_session() as session:
        yield session


async def create_database() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def purge_database() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
