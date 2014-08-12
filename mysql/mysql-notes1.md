#### 1 别名

```
mysql>  SELECT 
         ->  CONCAT(MONTHNAME(t),',',DAYOFMONTH(t),',',YEAR(t)),
       #->  DATE-FORMAT(t,'%M %e, %Y') AS 'Date of message',
         ->  name, size FROM mail; 
```

#### 2 合并多列构建复合值

```
SELECT
DATE-FORMAT(t,'%M %e, %Y') AS date_sent,
CONCAT(srcuser,'@',srchost) as sender,
CONCAT(dstuser,'@',dsthost) as recipient,
size FROM mail;
```

#### 3  COUNT (DISTINCT) 关键字优化查询结果

 ```
 SELECT COUT(DISTINCT) srcuser FROM mail;
 ```

 #### 4 试图来简化操作
 试图使一个虚拟的数据库表，并不包含实际的数据，可以看成是特定的SELECT语句
 先创建试图；

 ```
CREATE VIEW mail_view AS 
SELECT
DATE-FORMAT(t,'%M %e, %Y') AS date_sent,
CONCAT(srcuser,'@',srchost) as sender,
CONCAT(dstuser,'@',dsthost) as recipient,
size FROM mail;
 ```

在查询；

```
SELECT date_sent, sender, size FROM mail_view WHERE size > 1000 ORDER BY size;
```

 #### 5 多表查询
`join` 或者子查询

 ```
SELECT t1_id, name, size FROM table1 INNER JOIN table2 ON t1_id =  t2_id;

SELECT  * FROM table2 WHERE t2_id = (SELECT  t1_id FROM table1 name= "TOM" );
 ```

#### 6 从查询结果集头或尾取出部分行
`LIMIT` 结合 `ORDER BY`
场景：Web 中将一个跨越多个页面的查询结果划分为多次显示；
只返回合乎要求的那些查询结果行，避免带宽浪费；
`LIMIT`也可以及结合其他语句用于数据去冗余等操作；

```
# 头 n 行
SELECT * FROM table_test LIMIT 5;
SELECT * FROM table_test  ORDER BY name  (DESC) LIMIT 5;

# LIMIT 接受两个参数m，n；从m行开始，返回n行
SELECT * FROM table_test LIMIT 0,20;
SELECT * FROM table_test LIMIT 20,20;
SELECT * FROM table_test LIMIT 40,20;

# 返回若干行，并统计查询总结果
SELECT SQL_CALC_FOUND_ROWS * FROM table_test LIMIT 5;
SELECT FOUND_ROWS();

# 注意LIMIT避免将相同结果行分割，需要子查询
SELECT name, wins FROM al_winner 
WHERE wins >= (SELECT wins FROM al_winner ORDER BY wins DESC, name LIMIT 3,1)
ORDER BY wins DESC, name;
```