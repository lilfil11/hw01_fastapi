from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel
from time import time

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
    return f'You are in the root!'


# ваш код здесь
@app.post('/post')
def get_post():
    ts = Timestamp(id=len(post_db), timestamp=int(time()))
    post_db.append(ts)
    return ts


@app.get('/dog')
def get_dogs(kind: DogType):
    return [{'name': dog.name, 'pk': dog.pk, 'kind': dog.kind} for dog in dogs_db.values() if dog.kind == kind]


@app.post('/dog')
def create_dog(dog: Dog):
    dog.pk = len(dogs_db)
    dogs_db[dog.pk] = dog
    return dog


@app.get('/dog/{pk}')
def get_dog_by_pk(pk: int):
    return {'name': dogs_db[pk].name, 'pk': dogs_db[pk].pk, 'kind': dogs_db[pk].kind}


@app.patch('/dog/{pk}')
def update_dog(pk: int, dog: Dog):
    dog.pk = pk
    dogs_db[pk].name = dog.name
    dogs_db[pk].kind = dog.kind
    return dog