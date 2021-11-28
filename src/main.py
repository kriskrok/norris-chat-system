from fastapi import FastAPI, Request, HTTPException
import uvicorn
import os
import requests
from uvicorn.config import LOGGING_CONFIG
from pydantic import BaseModel

import PySimpleGUI as sg

app = FastAPI()

iplist = {}

class Item(BaseModel):
    ip: str

#fliptest = False
fliptest = True

is_host = True
host = '0.0.0.0'
port = 8000
if fliptest:
    is_host= False
    host = '0.0.0.1'
    port = 8001

@app.on_event("startup")
def connect_host():
    if not is_host:
        url = f"http://{os.environ['CHATHOST']}:8000/join"
        payload = {"ip": os.environ['MYIP']}
        response = requests.post(url, json=payload)
        print(response)

@app.post("/join")
async def post_root(payload: Item):
    if is_host:
        iplist.update({payload.ip: "nimimerkki"})
        print(iplist)
        return payload
    raise HTTPException(status_code=418, detail="I'm a teapot, not a host node")
        

@app.get("/")
def read_root():
    return "You should avoid notting be here \n It do be like that"

def run():
    LOGGING_CONFIG["formatters"]["default"]["fmt"] = "%(asctime)s [%(name)s] %(levelprefix)s %(message)s"
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    run()
