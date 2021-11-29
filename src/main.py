from fastapi import FastAPI, Request, HTTPException
import uvicorn
import os
import requests
from uvicorn.config import LOGGING_CONFIG
from pydantic import BaseModel

app = FastAPI()

iplist = {}

class Item(BaseModel):
    ip: str
 
host = os.environ['CHATHOST']
own_ip = os.environ['MYIP']
is_host = (host == '0.0.0.0')
localhost = '0.0.0.0'
port = 8000

@app.on_event("startup")
def connect_host():
    if not is_host:
        url = f"http://{host}:8000/join"
        payload = {"ip": own_ip}
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
    uvicorn.run(app, host=localhost, port=port)

if __name__ == "__main__":
    run()
