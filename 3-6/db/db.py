import logging
import psycopg 

# ADD channel_id PARSE
# INT the view count

#   post_id
#   channel_id
#   author_name
#   post_datetime
#   last_scrape_datetime
#   views INT
#   content_text
#   content_img

class Database:
    FLAGS = ["post_id", "post_link", "author_name", "author_link", "datetime", "last_scrape_datetime", "views", "content_text", "content_img"]

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")
        logging.getLogger("psycopg").setLevel(logging.DEBUG)


    def savePost(self, post: Post):
        pass

    def getPosts(self, args)