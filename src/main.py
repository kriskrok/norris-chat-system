from fastapi import FastAPI

app = FastAPI()

list = {}

@app.get("/list")
def read_list():
    print("hello")

@app.get("/add")
def add_counter():
    list.update({len(list): "hei"})
    return len(list)

@app.get("/")
def read_root():
    return "You should avoid notting be here \n It do be like that"