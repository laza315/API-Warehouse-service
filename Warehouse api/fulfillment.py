import time
from main import redis, Product
import logging


key = 'order-completed'
group = 'warehouse-group'

try:
    redis.xgroup_create(name=key, 
    groupname=group, mkstream=True)
    logging.info('Group created')
except Exception as exc:
    logging.warning(str(exc))

while True:
    try:
        results = redis.xreadgroup(groupname=group, 
                                   consumername=key,
                                   streams={key: '>'})
        logging.info(results)
        if results != []:
            for result in results:
                obj = result[1][0][1]
                try:
                    product = Product.get(obj['product_id'])
                    product.quantity -= int(obj['quantity'])
                    product.save()
                    logging.info(product)
                except: 
                    redis.xadd(name='refund-order', fields=obj)
    except Exception as exc:
        logging.warning(str(exc))
    time.sleep(3)
