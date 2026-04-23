from fastapi import FastAPI
from parser import parse

# ADD channel_id PARSE
# INT the view count

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/parse/{item_id}")
def read_item(item_id: int, q: str | None = None):
    # return {"item_id": item_id, "q": q}
    parse('@some_channel', o='out.csv', last=['5', 'd'], views=True, content_text=True)

    return 
