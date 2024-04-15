from typing import Annotated, Union
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os
import json
from loguru import logger
import sys
# import uvicorn
from fastapi.responses import StreamingResponse, RedirectResponse
from fastapi import FastAPI, File, WebSocket, BackgroundTasks, status, WebSocketDisconnect
import asyncio
import concurrent
import time
from contextlib import asynccontextmanager
import redis
from datetime import datetime, timedelta

# from utils.zeromq import ZeroMQSource 
from utils.sink import AsyncSinkRunner
from savant_rs.utils.serialization import load_message_from_bytes, Message
from collections import deque
import statistics
from pydantic import BaseModel


####################################### logger #################################
logger.remove()
logger.add(
    sys.stderr,
    colorize=True,
    format="<green>{time:HH:mm:ss}</green> | <level>{message}</level>",
    level=10,
)
logger.add("log.log", rotation="5 MB", level="DEBUG", compression="zip")


####################################### Variables #################################

class HistoryOnDateRange(BaseModel):
    date_from: float
    date_to: float
    source: str

connected_clients = set()
isOpenConn = False

class ConnectionManager:
    def __init__(self, q):
        self.active_connections: list[WebSocket] = []
        self.q = q

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
        
    async def receive_and_publish_message(self):
        while True:
            # await asyncio.sleep(0.01)
            data = await self.q.get()
            await self.broadcast(data)

q: asyncio.Queue = asyncio.Queue()
manager = ConnectionManager(q)
r = redis.Redis(host='redis', port=6379, decode_responses=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    loop = asyncio.get_event_loop()
    loop.create_task(zmq_connector(q))
    # manager.receive_and_publish_message()
    yield

app = FastAPI(title="Video inference module", lifespan=lifespan) #lifespan=lifespan


@app.websocket('/ws')
async def ws(websocket: WebSocket):
    await manager.connect(websocket)

    logger.debug(f"Connect client: {websocket}")
    try:
        await manager.broadcast(json.dumps("Client Connecte"))

        await manager.receive_and_publish_message()
        # while True:
            # data = await q.get()
            # await manager.broadcast(data)
    except Exception:
        manager.disconnect(websocket)


async def zmq_connector(q):
    runner = AsyncSinkRunner(
            socket="sub+connect:ipc:///tmp/zmq-sockets/output-video.ipc",
        )
    
    buf = deque(maxlen=30)
    
    # Create timer for upload data to redis if alert, no more than ones per second 
    sec = datetime.now() + timedelta(seconds=1)
    async for result in runner:
        # print(result.frame_meta)
        if result.frame_meta:
            # logger.debug(f"frame_meta: {result.frame_meta.get_all_objects()}")
            start_time = time.time()
            parced_list = []
            for i in result.frame_meta.get_all_objects():
                parced = {}
                parced['source_id'] = result.frame_meta.source_id
                parced['label'] = i.label
                parced['confidence'] = i.confidence
                parced['width'] = i.detection_box.width
                parced['height'] = i.detection_box.height
                parced['confidence'] = i.confidence
                parced_list.append(parced)
            buf.append(len(parced_list))
            mean_object_count = statistics.mean(buf)
            calc = {
                "source_id": result.frame_meta.source_id, 
                "object_count": len(parced_list), 
                "mean_object_count": mean_object_count, 
                "object_info": parced_list, 
                "alert": True if mean_object_count > 10 else False
            }

            # Send data to Redis stream
            if calc["alert"] and sec <= datetime.now():
                r.xadd(f"cam:{result.frame_meta.source_id}", 
                   {**calc, "object_info": json.dumps(calc["object_info"]), "alert": "alert"}
                )
                sec = datetime.now() + timedelta(seconds=1)

            logger.debug("--- %s seconds ---" % (time.time() - start_time))

            q.put_nowait(json.dumps(calc))

    logger.info(f"Done task")

@app.get("/", include_in_schema=False)
async def redirect():
    return RedirectResponse("/docs")


@app.get("/history")
async def redirect(req: HistoryOnDateRange):
    def date_to_ts(date):
        return int(time.mktime(date.timetuple()) * 1000)

    res4 = r.xrange(f"cam:{req.source}", date_to_ts(req.date_from), date_to_ts(req.date_to)) 
    
    logger.debug(len(res4))
    return res4


if __name__ == "__main__":
    print("run")
    # uvicorn.run("main:app", host="localhost", port=8000, reload=True, log_level="debug")




# async def zmq_connector():
#     def get_zmq():
#         context = zmq.Context()
#         socket = context.socket(zmq.SUB)
#         socket.connect("ipc:///tmp/zmq-sockets/output-video.ipc")  #tcp://host.docker.internal:5002 
#         socket.setsockopt(zmq.SUBSCRIBE, b'')
#         return socket

#     async def producer_handler(socket):
#         # assert isinstance(channel, PubSub)
        
#         while True:
#             await asyncio.sleep(0.01)
#             try:
#                 logger.debug(f"socket: {socket}")
#                 message = load_message_from_bytes(socket.recv()) # as_video_frame()
#                 logger.debug(message)
#                 if message:
#                     # for socket in connected_clients:
#                     #     try:
#                     #         socket.send_text(json.dumps(message))
#                     #     except:
#                     #         logger.debug("Socket closed before or while the server was sending a response.")
#                     logger.debug("Messages send!")
#             except Exception as exc:
#                 logger.error(exc)
#     socket = get_zmq()
#     await producer_handler(socket)
#     # done, pending = await asyncio.wait(
#     #     [producer_task], return_when=asyncio.FIRST_COMPLETED,
#     # )

#     logger.info(f"Done task")
#     # for task in pending:
#     #     logger.info(f"Canceling task: {task}")
#     #     task.cancel()

