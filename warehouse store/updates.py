import time
from main import redis, Order
import logging


key = 'refund-order'
group = 'payment'

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
                order = Order.get(obj['pk'])
                order.status = 'refunded'
                order.save()
                logging.info(order)
    except Exception as exc:
        logging.warning(str(exc))
    time.sleep(3)
