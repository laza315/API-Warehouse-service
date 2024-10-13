from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
from pydantic import BaseModel
import os
import uuid

app = FastAPI()

hosts = ['http://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins=hosts,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

redis = get_redis_connection(
    host='redis-10410.c300.eu-central-1-1.ec2.redns.redis-cloud.com', 
    port=10410,
    password='dCFrNDWab9PvHNGvsYTMD7aDHw7ay3dU',# os.environ.get('REDIS_PASSWORD_WAREHOUSE'),
    decode_responses=True
)

class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Config:
        arbitrary_types_allowed = True

    class Meta:
        database = redis  

@app.post('/product')
def create(product: Product):
    product_id = str(uuid.uuid4())  
    product.pk = product_id  
    product.save()
    return {"product_id": product_id}

@app.get('/product/{pk}')
def get(pk: str):
    return Product.get(pk)

@app.get('/products')
def all():
    return [format(pk) for pk in  Product.all_pks()]

def format(pk: str):
    product = Product.get(pk)
    return {'id': product.pk,
            'name': product.name,
            'quantity': product.quantity}

@app.delete('product/{pk}')
def delete(pk: str):
    return Product.delete(pk)