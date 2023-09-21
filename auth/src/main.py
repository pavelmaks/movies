from contextlib import asynccontextmanager

import uvicorn
from api.v1 import auth, history, role, user, oauth
from core import config
from db import redis
from fastapi import FastAPI
from redis.asyncio import Redis
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from fastapi_limiter import FastAPILimiter


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    redis.redis = Redis(host=config.settings.REDIS_HOST, port=config.settings.REDIS_PORT)
    await FastAPILimiter.init(redis.redis)

    yield

    # shutdown
    await redis.redis.close()


def configure_tracer() -> None:
    resource = Resource(attributes={"service.name": "movies-api"})
    trace.set_tracer_provider(TracerProvider(resource=resource))
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name=config.settings.JAEGER_HOST,
                agent_port=config.settings.JAEGER_PORT,
            )
        )
    )
    # Чтобы видеть трейсы в консоли
    # trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))

if config.settings.ENABLE_TRACER:
    configure_tracer()


app = FastAPI(
    title=config.settings.PROJECT_NAME,
    docs_url='/api/v1/auth/docs',
    openapi_url='/api/v1/auth/openapi.json',
    description="",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(auth.router, prefix='/api/v1/auth', tags=['auth'])
app.include_router(user.router, prefix='/api/v1/user', tags=['users'])
app.include_router(role.router, prefix='/api/v1/role', tags=['roles'])
app.include_router(history.router, prefix='/api/v1/history', tags=['history'])
app.include_router(oauth.router, prefix='/api/v1/oauth', tags=['oauth'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        reload=True,
    )
