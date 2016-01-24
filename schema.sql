drop table if exists users;
create table users (
  id integer primary key autoincrement,
  username text not null,
  password text not null
);
insert into users (username, password) values ('bryanmclellan', '1');
insert into users (username, password) values ('justin_mclellan', '1');
insert into users (username, password) values ('gnomes4dayz', '1');



drop table if exists history;
create table history (
  from_id text not null,
  to_id text not null,
  image_url text not null,
  image_id text not null
);


insert into history (from_id, to_id, image_url,image_id) values ('1', '2', "https://scontent.cdninstagram.com/hphotos-xat1/t51.2885-15/s640x640/sh0.08/e35/12107593_1042174985822373_1583369598_n.jpg", 1);
insert into history (from_id, to_id, image_url,image_id) values ('2', '3', "https://scontent.cdninstagram.com/hphotos-xta1/t51.2885-15/s640x640/sh0.08/e35/11856654_895560267148178_1167039240_n.jpg", 2);
insert into history (from_id, to_id, image_url,image_id) values ('3', '1', "https://scontent.cdninstagram.com/hphotos-xpf1/t51.2885-15/s640x640/sh0.08/e35/12269828_1139297556098452_646953286_n.jpg", 3);

