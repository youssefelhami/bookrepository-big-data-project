create database if not exists testdb;
use testdb;
create external table if not exists reviews (
  isbn bigint,
  rating string,
  review string,
  category string
)
row format delimited
fields terminated by ','
lines terminated by '\n'
stored as textfile location 'hdfs://namenode:8020/user/hive/warehouse/testdb.db/reviews';
