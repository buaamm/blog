drop table if exists users;
create table users (
    id integer primary key autoincrement,
    username text not null,
    password text not null,
    create_time text not null,
    nickname text not null,
    birthday text not null,
    sex integer not null,
    level integer not null,
    cash integer not null,
    description text not null
);

drop table if exists entries;
create table entries (
    id integer primary key autoincrement,
    userid integer not null,
    mid integer not null,
    title text not null,
    create_time text not null,
    abstract text not null,
    text text not null,
    mname text not null,
    mtype text not null,
    murls text not null
);

drop table if exists files;
create table files (
    id integer primary key autoincrement,
    userid integer not null,
    filename text not null,
    upload_time text not null,
    text text not null
);


drop table if exists items;
create table items (
    id integer primary key autoincrement,
    name text not null,
    type text not null,
    chapters integer not null,
    urls text not null,
    upload_time text not null,
    description text not null
);

drop table if exists images;
create table images (
    id integer primary key autoincrement,
    userid integer not null,
    name text not null,
    type text not null,
    count integer not null,
    urls text not null,
    upload_time text not null,
    description text not null
);


