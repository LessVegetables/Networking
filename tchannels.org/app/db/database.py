from datetime import datetime, timezone
from typing import List
from typing import Optional
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class Post(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int]
    channel_id: Mapped[str]
    author_name: Mapped[str]
    post_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    last_scrape_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    views: Mapped[int]
    content_text: Mapped[str]
    content_img: Mapped[list[str]] = mapped_column(ARRAY(String))

    def __repr__(self) -> str:
         return f"User(id={self.id!r}, name={self.post_id!r}, fullname={self.channel_id!r})"


from sqlalchemy import create_engine
# engine = create_engine("sqlite:///temp.db", echo=True)
engine = create_engine("postgresql+psycopg://danielgehrman:@localhost:5432/tchannels", echo=True)

Base.metadata.create_all(engine)

from sqlalchemy.orm import Session

with Session(engine) as session:
    posts = []

    for i in range(10):
        #scrapes 10 posts
        post = Post(
            post_id=25688,
            channel_id="d_code",
            author_name="Код Дурова",
            post_datetime=datetime(2026, 4, 28, 9, 30, 0, tzinfo=timezone.utc),
            last_scrape_datetime=datetime.now(timezone.utc),
            views=4670,
            content_text="Telegram теперь поддерживает...",
            content_img=[
                "https://cdn4.telegram-cdn.org/file/abc123.jpg",
                "https://cdn4.telegram-cdn.org/file/def456.jpg",
            ],
        )
        posts.append(post)

    session.add_all(posts)
    session.commit()


stmt = select(Post).where(Post.channel_id == "d_code")
with Session(engine) as session:
    for row in session.execute(stmt):
         print(row)