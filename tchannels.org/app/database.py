from datetime import datetime, timezone
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

    def __repr__(self) -> str:
         return f"Post(name={self.post_id!r}, fullname={self.channel_id!r})"

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