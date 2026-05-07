from datetime import datetime, timezone, timedelta
from typing import List
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker


# metadata_obj = MetaData()

# tchannels_table = Table(
#     "tchannels",
#     metadata_obj,
#     Column("id", mapped_column(Integer), primary_key=True),
#     Column("post_id", mapped_column(Integer)),
#     Column("channel_id", mapped_column(String)),
#     Column("author_name", mapped_column(String)),
#     Column("post_datetime", mapped_column(DateTime(timezone=True))),
#     Column("last_scrape_datetime", mapped_column(DateTime(timezone=True))),
#     Column("views", mapped_column(Integer)),
#     Column("content_text", mapped_column(String)),
#     Column("content_img", mapped_column(ARRAY(String))),
# )

class Base(DeclarativeBase):
    # metadata = metadata_obj
    pass

class Post(Base):
    __tablename__ = "posts"
    # id: Mapped[int]
    post_id: Mapped[str] = mapped_column(unique=True, primary_key=True)
    channel_id: Mapped[str]
    author_name: Mapped[str]
    post_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    last_scrape_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    views: Mapped[int]
    content_text: Mapped[str]
    content_img: Mapped[list[str]] = mapped_column(ARRAY(String))

    FIELDS = {
        "post_id":              lambda self: self.post_id,
        "channel_id":           lambda self: self.channel_id,
        "author_name":          lambda self: self.author_name,
        "post_datetime":        lambda self: self.post_datetime,
        "last_scrape_datetime": lambda self: self.last_scrape_datetime,
        "views":                lambda self: self.views,
        "content_text":         lambda self: self.content_text,
        "content_img":          lambda self: self.content_img,
    }

    def __repr__(self):
        return f"Post(post_id={self.post_id!r}, post_datetime={self.post_datetime!r})"
    
    def to_dict(self, wanted: set[str] = None): # -> dict:
        if len(wanted) == 0:
            fields = self.FIELDS
        else:
            fields = {k: v for k, v in self.FIELDS.items() if k in wanted }
        return {k: fn(self) for k, fn in fields.items()}

# engine = create_engine("sqlite:///temp.db", echo=True)
engine = create_engine("postgresql+psycopg://danielgehrman:@localhost:5432/tchannels", echo=True)

Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

def post_exists(post):
    with SessionLocal() as session:
        stmt = select(Post).where(Post.post_id == post.post_id)
        row = session.execute(stmt)
        if len(row) == 0:
            return 0
        else:
            return 1

# def add_post(post):
#     with SessionLocal() as session:
#         stmt = select(Post).where(Post.post_id == post.post_id)
#         existing_post = session.scalars(stmt).first()
#         if existing_post is None:
#             session.add(post) # just add, no update
#         else:
#             #we update
#             existing_post = post
#             session.execute(select(Post.post_id)) #autoflush 
#         session.commit()

def return_posts(channel, params, last):
    value, unit = int(last[0]), last[1]

    result = {"posts": []}

    print(f"{set(params.keys())=}")
    
    # if len(params_keys) != 0:
    #     with SessionLocal() as session:
    #         columns = [getattr(Post, k) for k in params_keys]
    #         for col in columns:
    #             print(f"{col=}")
    #         stmt = select(*columns).where(str(Post.channel_id) == channel)
    #         rows = session.scalars(stmt).all()
    # else:

    with SessionLocal() as session:        

        stmt = select(Post).where(Post.channel_id == channel).order_by(Post.post_datetime.desc())

        if unit == 'p':
            stmt = stmt.limit(value)
        elif unit in ('h', 'd'):
            if unit == 'h':
                delta = timedelta(hours=value)
            else:
                delta = timedelta(days=value)
            stmt = stmt.where(Post.post_datetime >= datetime.now(timezone.utc) - delta)

        rows = session.scalars(stmt).all()
    
    result["posts"] = [row.to_dict(wanted=set(params.keys())) for row in rows]

    return result
