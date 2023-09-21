from contextlib import asynccontextmanager

import uvicorn
from api.v1 import films, genres, persons
from core import config
from db import elastic, redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends, FastAPI, Request, status
from fastapi.responses import ORJSONResponse
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from redis.asyncio import Redis
from services.auth import all_access


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    redis.redis = Redis(host=config.settings.REDIS_HOST, port=config.settings.REDIS_PORT)
    elastic.es = AsyncElasticsearch(hosts=[f'{config.settings.ELASTIC_HOST}:{config.settings.ELASTIC_PORT}'])
    yield
    # shutdown
    await redis.redis.close()
    await elastic.es.close()


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
    docs_url='/api/v1/movies/docs',
    openapi_url='/api/v1/movies/openapi.json',
    description="Информация о фильмах, жанрах и людях, участвовавших в создании произведения",
    version="1.0.0",
    lifespan=lifespan,
    dependencies=[Depends(all_access)],
)

FastAPIInstrumentor.instrument_app(app)


@app.middleware('http')
async def before_request(request: Request, call_next):
    response = await call_next(request)
    request_id = request.headers.get('X-Request-Id')
    if not request_id:
        return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'detail': 'X-Request-Id is required'})
    return response


app.include_router(films.router, prefix='/api/v1/films', tags=['films'])
app.include_router(genres.router, prefix='/api/v1/genres', tags=['genres'])
app.include_router(persons.router, prefix='/api/v1/persons', tags=['persons'])

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000)
