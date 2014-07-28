### sysbench 测试
#### 1 cpu 性能测试
```
sysbench --test=cpu --cpu-max-prime=20000 run
```

cpu测试主要是进行素数的加法运算，在上面的例子中，
指定了最大的素数为 20000，自己可以根据机器cpu的性能来适当调整数值。

```
sysbench 0.4.10:  multi-threaded system evaluation benchmark

Running the test with following options:
Number of threads: 1

Doing CPU performance benchmark

Threads started!

Done.

Maximum prime number checked in CPU test: 20000


Test execution summary:
    total time:                          30.5083s
    total number of events:              10000
    total time taken by event execution: 30.5043
    per-request statistics:
         min:                                  2.83ms
         avg:                                  3.05ms
         max:                                  6.46ms
         approx.  95 percentile:               3.48ms

Threads fairness:
    events (avg/stddev):           10000.0000/0.00
    execution time (avg/stddev):   30.5043/0.00
```

#### 2 线程测试

```
sysbench --test=threads --num-threads=64 --thread-yields=100 --thread-locks=2 run
```

```
sysbench 0.4.10:  multi-threaded system evaluation benchmark

Running the test with following options:
Number of threads: 64

Doing thread subsystem performance test
Thread yields per test: 100 Locks used: 2
Threads started!
Done.


Test execution summary:
    total time:                          0.6215s
    total number of events:              10000
    total time taken by event execution: 39.3849
    per-request statistics:
         min:                                  0.04ms
         avg:                                  3.94ms
         max:                                 85.26ms
         approx.  95 percentile:              30.41ms

Threads fairness:
    events (avg/stddev):           156.2500/10.52
    execution time (avg/stddev):   0.6154/0.00
```

#### 3 磁盘IO性能测试，随机读写和删除

```
sysbench --test=fileio --num-threads=16 --file-total-size=3G --file-test-mode=rndrw prepare
sysbench --test=fileio --num-threads=16 --file-total-size=3G --file-test-mode=rndrw run
sysbench --test=fileio --num-threads=16 --file-total-size=3G --file-test-mode=rndrw cleanup
```

上述参数指定了最大创建16个线程，创建的文件总大小为3G，文件读写模式为随机读。

```
sysbench 0.4.10:  multi-threaded system evaluation benchmark

Running the test with following options:
Number of threads: 64

Doing thread subsystem performance test
Thread yields per test: 100 Locks used: 2
Threads started!
Done.


Test execution summary:
    total time:                          0.6215s
    total number of events:              10000
    total time taken by event execution: 39.3849
    per-request statistics:
         min:                                  0.04ms
         avg:                                  3.94ms
         max:                                 85.26ms
         approx.  95 percentile:              30.41ms

Threads fairness:
    events (avg/stddev):           156.2500/10.52
    execution time (avg/stddev):   0.6154/0.00

```

```
sysbench 0.4.10:  multi-threaded system evaluation benchmark

Running the test with following options:
Number of threads: 16

Extra file open flags: 0
128 files, 24Mb each
3Gb total file size
Block size 16Kb
Number of random requests for random IO: 10000
Read/Write ratio for combined random IO test: 1.50
Periodic FSYNC enabled, calling fsync() each 100 requests.
Calling fsync() at the end of test, Enabled.
Using synchronous I/O mode
Doing random r/w test
Threads started!
FATAL: Failed to read file! file: 3 pos: 0 errno = 0 (Q?)
FATAL: Failed to read file! file: 3 pos: 6340608 errno = 0 ()
FATAL: Failed to read file! file: 13 pos: 16531456 errno = 0 ()
FATAL: Failed to read file! file: 48 pos: 5537792 errno = 0 ()
FATAL: Failed to read file! file: 96 pos: 8503296 errno = 0 ()
FATAL: Failed to read file! file: 26 pos: 9568256 errno = 0 ()
FATAL: Failed to read file! file: 26 pos: 15794176 errno = 0 ()
FATAL: Failed to read file! file: 127 pos: 18300928 errno = 0 ()
FATAL: Failed to read file! file: 9 pos: 21331968 errno = 0 ()
FATAL: Failed to read file! file: 119 pos: 8421376 errno = 0 ()
FATAL: Failed to read file! file: 62 pos: 17448960 errno = 0 ()
FATAL: Failed to read file! file: 87 pos: 20398080 errno = 0 ()
FATAL: Failed to read file! file: 113 pos: 13156352 errno = 0 ()
FATAL: Failed to read file! file: 20 pos: 10649600 errno = 0 ()
FATAL: Failed to read file! file: 17 pos: 9060352 errno = 0 ()
FATAL: Failed to read file! file: 16 pos: 311296 errno = 0 ()
Done.

Operations performed:  0 Read, 0 Write, 0 Other = 0 Total
Read 0b  Written 0b  Total transferred 0b  (0b/sec)
    0.00 Requests/sec executed

Test execution summary:
    total time:                          0.0029s
    total number of events:              0
    total time taken by event execution: 0.0000
    per-request statistics:
         min:                            18446744073709.55ms
         avg:                                  0.00ms
         max:                                  0.00ms

Threads fairness:
    events (avg/stddev):           0.0000/0.00
    execution time (avg/stddev):   0.0000/0.00
```


```
sysbench 0.4.10:  multi-threaded system evaluation benchmark

Removing test files...
```

#### 4 内存测试

```
sysbench --test=memory --memory-block-size=8k --memory-total-size=4G run
```

上述参数指定了本次测试整个过程是在内存中传输 4G 的数据量，每个 block 大小为 8K。

```
```


#### 5 mysql 性能测试
##### prepare data

```
sysbench --test=oltp --mysql-table-engine=innodb --oltp-table-size=1000000 \
--mysql-socket=/home/data/mysql/mysql.sock --mysql-user=root --mysql-host=localhost \
--mysql-password=123456 --mysql-db=students --oltp-table-name=test prepare
```



```
sysbench 0.4.10:  multi-threaded system evaluation benchmark

No DB drivers specified, using mysql
Creating table 'test'...
Creating 1000000 records in table 'test'...
```

##### run test

```
sysbench --test=oltp --mysql-table-engine=innodb --oltp-table-size=1000000 \
--mysql-socket=/home/data/mysql/mysql.sock --mysql-user=root --mysql-host=localhost \
--mysql-password=123456 --mysql-db=students --oltp-table-name=test \
--max-requests=1000 --num-threads=100 run
```

```
sysbench 0.4.10:  multi-threaded system evaluation benchmark

No DB drivers specified, using mysql
WARNING: Preparing of "BEGIN" is unsupported, using emulation
(last message repeated 99 times)
Running the test with following options:
Number of threads: 100

Doing OLTP test.
Running mixed OLTP test
Using Special distribution (12 iterations,  1 pct of values are returned in 75 pct cases)
Using "BEGIN" for starting transactions
Using auto_inc on the id column
Maximum number of requests for OLTP test is limited to 1000
Threads started!
Done.

OLTP test statistics:
    queries performed:
        read:                            14000
        write:                           5000
        other:                           2000
        total:                           21000
    transactions:                        1000   (276.21 per sec.)
    deadlocks:                           0      (0.00 per sec.)
    read/write requests:                 19000  (5247.91 per sec.)
    other operations:                    2000   (552.41 per sec.)

# 时间统计信息（最小，平均，最大响应时间，以及95%百分比响应时间）
Test execution summary:
    total time:                          3.6205s
    total number of events:              1000
    total time taken by event execution: 356.3231
    per-request statistics:
         min:                                 55.01ms
         avg:                                356.32ms
         max:                               1223.34ms
         approx.  95 percentile:             764.73ms

# 线程公平性统计信息
Threads fairness:
    events (avg/stddev):           10.0000/0.76
    execution time (avg/stddev):   3.5632/0.03
```

###### 参数解释
1.  --max-requests --max-requests 默认值为10000 ，如果设置了--max-requests 或者使用默认值 ，分析结果的时候主要查看运行时间(total time)，一般情况下，都将--max-requests 赋值为0 ，即不限制请求数量，通过--max-time 来指定测试时长，然后查看系统的每秒事务数。

2.  --oltp-test-mode用以指定测试模式，取值有(simeple,complex,nontrx)，默认是complex。不同模式会执行不同的语句。 具体执行语句如下所示：

```
# Simple
SELECT c FROM sbtest WHERE id=N

# Complex(Advanced transactional) 在事务中，可能包含下列语句。
SELECT c FROM sbtest WHERE id=N
SELECT c FROM sbtest WHERE id BETWEEN N AND M
SELECT SUM(K) FROM sbtest WHERE id BETWEEN N and M
SELECT c FROM sbtest WHERE id between N and M ORDER BY c
SELECT DISTINCT c FROM sbtest WHERE id BETWEEN N and M ORDER BY c
UPDATE sbtest SET k=k+1 WHERE id=N
UPDATE sbtest SET c=N WHERE id=M
DELETE FROM sbtest WHERE id=N
INSERT INTO sbtest VALUES (...)

# nontrx(Non-transactional) 这种模式包含下列SQL语句。
SELECT pad FROM sbtest WHERE id=N
UPDATE sbtest SET k=k+1 WHERE id=N
UPDATE sbtest SET c=N WHERE id=M
DELETE FROM sbtest WHERE id=N
INSERT INTO sbtest (k, c, pad) VALUES(N, M, S)
```

3.  simple 与 --oltp-read-only 的区别; simple模式和在complex模式下开启read-only选项都只包含select语句。但是 simple模式只包含最简单的select语句，相反地，complex 模式中，如果我们开启read-only 选项，即--oltp-read-only=on，则会包含复杂的SQL语句。如：

```
SELECT SUM(K) FROM sbtest WHERE id BETWEEN N and M
 SELECT DISTINCT c FROM sbtest WHERE id BETWEEN N and M ORDER BY c
```

##### clean data

```
sysbench --test=oltp --mysql-host=localhost  --mysql-user=root  --mysql-password=123456 \
--mysql-socket=/home/data/mysql/mysql.sock --mysql-db=students --oltp-table-name=test cleanup
```

以上测试内容参考 [MySQL 中文网](http://imysql.cn/node/312)， 结果为一台1核1G主机的性能测试结果。

除了测试oltp，sysbench 0.5还可以进行插入操作的性能测试(insert.lua)，选择操作的性能测试(select.lua)等。

1. [1](http://blog.csdn.net/clh604/article/details/12108477)
2. [2](http://wenku.baidu.com/view/f0ae451414791711cc7917ba.html)
3. [3](http://www.linuxidc.com/Linux/2012-11/75054p2.htm)
4. [4:sysbench(oltp测试)使用说明](http://www.cnblogs.com/minglog/archive/2011/05/10/2042143.html)