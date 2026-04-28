from fastapi import FastAPI, Request
from parser import parse

# ADD channel_id PARSE
# INT the view count
FLAGS = ["post_id", "post_link", "author_name", "author_link", "datetime", "last_scrape_datetime", "views", "content_text", "content_img"]

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/parse/{channel}")
def read_item(channel: str, request: Request):


    params = dict(request.query_params)

    params_keys = list(params.keys())

    for k in params_keys:
        if k in FLAGS:
            params[k] = True
        else:
            params.pop(k)
    
    d = request.query_params.get("d")

    parse(f'@{channel}', o='out.csv', last=['5', 'd'], flags=params)

    return {"parsed channel": channel, "params": params}


# @app.post("/parse/{channel}")