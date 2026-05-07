from fastapi import FastAPI, Request
from parser import parse

from database import SessionLocal, post_exists, return_posts
from database import Post as DbPost

# ADD channel_id PARSE
# INT the view count
FLAGS = ["post_id", "post_link", "author_name", "author_link", "datetime", "last_scrape_datetime", "views", "content_text", "content_img", "last"]

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/parse/{channel}")
def parse_channel(channel: str, last: str = "10p"):
    # parse the channel (scrap all the data), returns an array of Post objects
    # add/update to the database
    # return a 200

    value, unit = last[:-1], last[-1]

    # for k in params_keys:
    #     if k in FLAGS:
    #         params[k] = True
    #     else:
    #         params.pop(k)
    
    # d = request.query_params.get("d")

    posts = parse(f'@{channel}', o='out.csv', last=[value, unit])

    posts = [DbPost(**post.to_db()) for post in posts]

    # for post in posts:
    #     add_post(post)
    with SessionLocal() as session:
        for post in posts:
            session.merge(post)
        session.commit()


    return {"parsed channel": channel, "last": last}

@app.get("/data/{channel}")
def read_postst_from_channel(channel: str, request: Request, last: str = "10p"):
    # get list(Post) of posts
    # return 500smth if posts dating n hours/days back don't exist
    # serialize all the posts
    # return 200 with json

    params = dict(request.query_params)

    params_keys = list(params.keys())

    for k in params_keys:
        if k in FLAGS:
            if k == 'last':
                params.pop(k)
                continue
            params[k] = True
        else:
            params.pop(k)
    
    # d = request.query_params.get("d")
    print(f"\t{channel=}\n\t{params=}\n\t{last=}")
    result = return_posts(channel, params, last) ################################################


    # with SessionLocal() as session:
    #         from sqlalchemy import select
    #         stmt = select(DbPost) #.where(DbPost.channel_id == channel)
    #         result = session.scalars(stmt).first()

    # parse(f'@{channel}', o='out.csv', last=['5', 'd'], flags=params)
    # return {"parsed channel": channel, "params": params}
    
    print(f"{len(result["posts"])=}")
    return result
