# import zmq
# context = zmq.Context()
# socket = context.socket(zmq.SUB)
# socket.connect("tcp://host.docker.internal:5002")
# socket.setsockopt(zmq.SUBSCRIBE, b'')
# for request in range(10):
#     print("Wait message")
#     message = socket.recv_pyobj()
#     print(message)
#     print("")

import redis 
import json
from datetime import datetime, timedelta
import time
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# assert r.ts().create("time-series-1")
# assert r.ts().add("time-series-1", 3, 50)

# res1 = r.xadd(
#     "cam:one",
#     {"rider": "Castilla", "speed": 1, "position": json.dumps([{"rider": "Castilla", "speed": 1}]), "location_id": 10},
# )
# print(res1) 
print(f"{(datetime.now()-timedelta(days=1)).strftime('%s')}-0",  f"{datetime.now().strftime('%s')}-0")
def date_to_ts(date):
    return int(time.mktime(date.timetuple()) * 1000)
print(date_to_ts(datetime.now()-timedelta(days=1)))
res4 = r.xrange("cam:test", date_to_ts(datetime.now()-timedelta(minutes=50)), date_to_ts(datetime.now())) 
# f"{(datetime.now()-timedelta(days=1)).strftime('%s')}",  f"{datetime.now().strftime('%s')}"
print(len(res4))

#  1710061807618 - 1710061828061
#  1710064736000