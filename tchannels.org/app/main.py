from fastapi import FastAPI, Request
from parser import parse

# ADD channel_id PARSE
# INT the view count

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/parse/{channel}")
def read_item(channel: str, request: Request):

    parse(f'@{channel}', o='out.csv', last=['5', 'd'], views=True, content_text=True)

    params = dict(request.query_params)
    d = request.query_params.get("d")

    return {"parsed channel": channel, "params": params}


# @app.post("/parse/{channel}")