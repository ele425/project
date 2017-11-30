drop table if exists fingerprints;
drop table if exists songs;

create table fingerprints (
  hash_id int not null auto_increment primary key,
  hash_path varchar(80)
);

create table songs (
  song_id int not null auto_increment primary key,
  song_name varchar(20),
  song_artist varchar(20)
);
