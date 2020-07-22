CREATE SCHEMA categories

CREATE TABLE categories.category (
  id integer NOT NULL GENERATED BY DEFAULT AS IDENTITY,
  name text NOT NULL,
  info text,
  parent_id integer,
  CONSTRAINT pk_category PRIMARY KEY (id)
)

CREATE SCHEMA users

CREATE TABLE users.user (
  chat_id integer NOT NULL,
  first_name text,
  last_name text,
  is_admin boolean,
  state text,
  CONSTRAINT pk_user PRIMARY KEY (id)
)