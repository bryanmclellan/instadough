drop table if exists users;
create table users (
  id integer primary key autoincrement,
  username text not null,
  password text not null,
  nessie_id text
);
insert into users (username, password) values ('insta', 'dough');
insert into users (username, password) values ('Chris', 'Fralic');
insert into users (username, password) values ('Donald', 'Trump');

drop table if exists history;
create table history (
  from_id text not null,
  to_id text not null,
  image_url text not null,
  image_id text not null
);
