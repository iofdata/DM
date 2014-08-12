### 4 表管理

#### 4.1 克隆表

```
CREATE TABLE new LIKE old;  # 不克隆外键定义，不克隆 DATA 和 INDEX DIRECTORY
INSERT INTO new SELECT * FROM old; # 拷贝数据
```

#### 4.2 将查询结果保存到表中
场景： 临时表用于调试；安全起见；提高效率；
            大的存储表和小的工作表；
            多次操作，临时表效率可能更高；

```
INSERT INTO dst_tbl (i,s) SELECT id, name FROM src_tbl;
INSERT INTO dst_tbl (i,s) SELECT COUNT(*), name FROM src_tbl GROUP BY name;

# INSERT 之前需要创建表
CREATE TABLE dst_tbl SELECT a,b,c FROM src_tbl;
```