"""
Dummy api routes to demonstrate the code instrumentation
"""

import random
import time

import httpx
from fastapi.routing import APIRouter

dummy_router = APIRouter()


# Example endpoint
@dummy_router.get("/")
async def read_root():
    import pudb

    pudb.set_trace()
    print(__file__)
    time.sleep(random.randint(2, 5))
    return {"message": "Hello, OpenTelemetry!"}


@dummy_router.get("/slow")
async def slow():
    time.sleep(random.randint(10, 15))
    random_payload = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=100))
    return {"message": "Hello, OpenTelemetry!", "payload": random_payload}


@dummy_router.get("/not-working")
async def not_working():
    # time.sleep(random.randint(10, 15))
    random_payload = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=100))
    raise ValueError('something went wrong')
    return {"message": "Hello, OpenTelemetry!", "payload": random_payload}


@dummy_router.get("/call-with-httpx")
async def call_with_httpx():
    url = "https://jsonplaceholder.typicode.com/posts"
    response = httpx.get(url)

    return {"message": "Hello, OpenTelemetry!", "httpx_response": response.json()}


@dummy_router.get("/call-with-httpx-async")
async def call_with_httpx_async():
    url = "https://jsonplaceholder.typicode.com/posts"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    return {"message": "Hello, OpenTelemetry!", "httpx_response": response.json()}
