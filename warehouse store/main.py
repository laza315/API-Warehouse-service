from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
from pydantic import BaseModel
import os
import requests
import time
from fastapi.background import BackgroundTasks

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

class ProductOrder(HashModel):
    product_id: str 
    quantity: int 
    class Meta:
        database = redis

class Order(HashModel):
    product_id: str 
    price: float 
    fee: float
    total: float 
    quantity: int
    status: str 
    class Meta: 
        database = redis
        
@app.post('/oders')
def create(productOrder: ProductOrder, backgorund_tasks: BackgroundTasks):
    req = requests.get(f'http://localhost:8000/products/{productOrder.product_id}')
    product = req.json()
    fee = product['price'] * 0.2

    order = Order(
        product_id = productOrder.product_id,
        price = product['price'],
        fee = fee,
        total = product['price'] + fee,
        quantity = productOrder.quantity,
        status = 'pending'
    )
    order.save()

    backgorund_tasks.add_task(order_complete, order)

    return order.save()

@app.get('/orders/{pk}')
def get(pk: str):
    return format(pk)

@app.get('/orders')
def get_all():
    return [format(pk) for pk in Order.all_pks()]

def format(pk: str):
    order = Order.get(pk)
    return {
        'id': order.pk,
        'product_id': order.product_id,
        'fee': order.fee,
        'total': order.total,
        'quantity': order.quantity,
        'status': order.status
    }


def order_complete(order: Order):
    time.sleep(5)
    order.status = 'completed'
    order.save()
    redis.xadd(name='order-completed', fields=order.dict())