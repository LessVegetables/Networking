-- https://docs.docker.com/guides/pre-seeding/
-- seed.sql

CREATE DATABASE tchannels;

\c tchannels

CREATE TABLE posts (
  post_id SERIAL PRIMARY KEY, -- d_code/25688
  channel_id VARCHAR(32),-- d_code
  author_name VARCHAR(100), -- Код Дурова
  post_datetime TIMESTAMP WITH TIME ZONE,
  last_scrape_datetime TIMESTAMP WITH TIME ZONE,
  views INT, --4.67K
  content_text TEXT, 
  content_img TEXT ARRAY[10]
  -- reactions
);