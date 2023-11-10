from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from time import time
from typing import List, Dict

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get('/')
def root():
    # ваш код здесь
    return 'You are in the root!'


# ваш код здесь
@app.post('/post')
def get_post() -> Timestamp:
    ts = Timestamp(id=len(post_db), timestamp=int(time()))
    post_db.append(ts)
    return ts


@app.get('/dog')
def get_dogs(kind: DogType = None) -> List[Dog]:
    dogs = [dog for dog in dogs_db.values() if dog.kind == kind]
    
    if dogs:
        return dogs

    return list(dogs_db.values())


@app.post('/dog')
def create_dog(dog: Dog) -> Dog:
    if dog.pk in dogs_db:
        raise HTTPException(status_code=409, detail='The specified PK already exists.')

    dogs_db[dog.pk] = dog
    return dog


@app.get('/dog/{pk}')
def get_dog_by_pk(pk: int) -> Dog:
    return dogs_db[pk]


@app.patch('/dog/{pk}')
def update_dog(pk: int, dog: Dog) -> Dog:
    if pk not in dogs_db:
        raise HTTPException(status_code=409, detail="Dog with the entered PK doesn't exist.")
    elif pk != dog.pk:
        raise HTTPException(status_code=409, detail='The entered PK do not match.')

    dogs_db[pk].name = dog.name
    dogs_db[pk].kind = dog.kind
    return dog