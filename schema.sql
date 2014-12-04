drop table if exists entries;
create table entries (
    id integer primary key autoincrement,
    userid integer not null,
    title text not null,
    create_time text not null,
    text text not null
);

drop table if exists files;
create table files (
    id integer primary key autoincrement,
    userid integer not null,
    filename text not null,
    upload_time text not null,
    text text not null
);


drop table if exists users;
create table users (
    id integer primary key autoincrement,
    username text not null,
    password text not null,
    create_time text not null,
    birthday text,
    sex integer,
    description text
);
