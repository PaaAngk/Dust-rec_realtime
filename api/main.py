from dotenv import load_dotenv
import os
import json
from loguru import logger
import sys
from fastapi.responses import StreamingResponse, RedirectResponse
from fastapi import FastAPI, File, WebSocket, BackgroundTasks, status, WebSocketDisconnect
import time
from contextlib import asynccontextmanager
import redis
from datetime import datetime, timedelta
from pydantic import BaseModel
import uvicorn
import pandas as pd
import math
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
DEBUG = os.getenv("DEBUG") == "True"

####################################### logger #################################
logger.remove()
logger.add(
    sys.stderr,
    colorize=True,
    format=os.getenv("LOGGING_FORMAT"),
)
logger.add("api.log", rotation=os.getenv("LOGGING_ROTATION"), level=os.getenv("LOGGING_LEVEL"), compression='zip')


####################################### Variables #################################

class HistoryOnDateRange(BaseModel):
    date_from: float
    date_to: float
    source: str

origins = [
    "http://localhost",
    "http://localhost:4200",
]


r = redis.Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"), decode_responses=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # manager.receive_and_publish_message()
    yield
    # del r

app = FastAPI(title="Video inference module", lifespan=lifespan) #lifespan=lifespan

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", include_in_schema=False)
async def redirect():
    return RedirectResponse("/docs")


@app.get("/history/") # req: HistoryOnDateRange
async def redirect(source: str, timestamp_from:int, timestamp_to:int):
    logger.debug(source, timestamp_from, timestamp_to)
    res4 = r.xrange(f"cam:{source}", timestamp_from, timestamp_to) # date_to_ts(req.date_to)
    result = get_periods(res4)
    logger.debug(len(result))
    return result


def date_to_ts(date):
        return int(time.mktime(date.timetuple()) * 1000)

def get_periods(arr):
    date_time_list = []
    for i in arr:
        ts = i[0].split('-')[0]
        date = datetime.fromtimestamp(math.floor(int(ts)/1000))
        date_time_list.append({
            "date": date,
            "data": i
        })
    df = pd.DataFrame(date_time_list)

    df["first"] = df["date"].diff().dt.seconds > 3
    df["sec"] = df["date"].diff().dt.seconds
    df["last"] = df['first'].shift(-1)

    sorted_df = df[(df['first'] == True) | df['last'] == True].to_numpy()
    result = []
    for i, row in enumerate(sorted_df):
        if i+1 < len(sorted_df):
            next_row = sorted_df[i+1]
            if row[2] == True and next_row[2] == False and next_row[3] == 1: 
                # print(next_row)
                result.append({
                    "dateFrom": row[0],
                    "dateTo": next_row[0],
                    "metadataFrom": row[1][1],
                    "metadataTo": next_row[1][1],
                    "duration": (next_row[0] - row[0]).total_seconds(),
                })
    return result


if __name__ == "__main__":
    # print("run")
    uvicorn.run("main:app", host="localhost", port=8004, reload=True, log_level="debug")
