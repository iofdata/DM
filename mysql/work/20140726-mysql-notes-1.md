

### A 数据表大小查询
```
# 1、进去指定schema 数据库（存放了其他的数据库的信息）
mysql> use information_schema;

# 2、查询所有数据的大小  
mysql> select concat(round(sum(DATA_LENGTH/1024/1024), 2), 'MB') as data from TABLES;

+-----------+
| data      |
+-----------+
| 1948.72MB |
+-----------+
1 row in set (0.31 sec)

# 3、查看指定数据库实例的大小，比如说数据库 forexpert 
mysql> select concat(round(sum(DATA_LENGTH/1024/1024), 2), 'MB')
         -> as data from TABLES where table_schema='students';

+-----------+
| data      |
+-----------+
| 1948.02MB |
+-----------+
1 row in set (0.00 sec)

# 4、查看指定数据库的表的大小，比如说数据库 forexpert 中的 member 表
 mysql> select concat(round(sum(DATA_LENGTH/1024/1024),2),'MB') 
          -> as data from TABLES where table_schema='students'
          -> and table_name='test';

+-----------+
| data      |
+-----------+
| 1948.00MB |
+-----------+
1 row in set (0.00 sec)
```