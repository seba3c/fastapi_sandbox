import json
import random
from collections.abc import AsyncIterable, Iterable
from typing import List

import orjson
from fastapi import APIRouter, Query
from pydantic import BaseModel

router = APIRouter(tags=["health"])


class Item(BaseModel):
    name: str
    description: str | None


_all_items = [
    Item(name="Plumbus", description="A multi-purpose household device."),
    Item(name="Portal Gun", description="A portal opening device."),
    Item(name="Meeseeks Box", description="A box that summons a Meeseeks."),
    Item(name="Microverse Battery", description="A battery powered by a miniature universe."),
    Item(name="Mega Seeds", description="Seeds from Mega Fruit, for smuggling past customs."),
    Item(name="Concentrated Dark Matter", description="Fuel that powers faster-than-light travel."),
    Item(name="Neutrino Bomb", description="A bomb that only destroys organic matter."),
    Item(name="Shrink Ray", description="A ray gun that shrinks its target."),
    Item(name="Memory Eraser", description="A device that erases short-term memories."),
    Item(name="Freeze Ray", description="A ray gun that freezes its target solid."),
]

def random_items(n: int) -> list[Item]:
    return random.choices(_all_items, k=n)

items = random_items(50000)

def get_random_items(n: int = Query(default=3, ge=1, le=100000)) -> list[Item]:
    return random_items(n)

@router.get("/items/no-stream")
async def no_stream_items() -> List[Item]:
    return items

@router.get("/items/concat-and-json")
async def concat_items():
    response = '['
    for item in items:
        str_item = f'{{ "name": "{item.name}", "description": "{item.description}" }},'
        response += str_item
    response = response[:-1]
    response += ']'
    return json.loads(response)

@router.get("/items/list-and-orjson")
async def concat_items():
    response = []
    for item in items:
        str_item = f'{{ "name": "{item.name}", "description": "{item.description}" }}'
        response.append(str_item)
    response = "[" + ",".join(response) + "]"
    return orjson.loads(response)

@router.get("/items/stream")
async def stream_items() -> AsyncIterable[Item]:
    for item in items:
        yield item

@router.get("/items/stream-no-async")
def stream_items_no_async() -> Iterable[Item]:
    for item in items:
        yield item


@router.get("/items/stream-no-annotation")
async def stream_items_no_annotation():
    for item in items:
        yield item

@router.get("/items/stream-no-async-no-annotation")
def stream_items_no_async_no_annotation():
    for item in items:
        yield item
