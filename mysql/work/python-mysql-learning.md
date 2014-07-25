### 1 登录及管理
```
mysql -h localhost -p -u root
mysql> GRANT ALL ON mysqlcookbook TO 'tom'@'localhost' IDENTIFIED   BY 'cbpass'
mysql> GRANT ALL ON pythoncookbook TO 'ana'@'xyz.com' IDENTIFIED   BY 'cbpass'
mysql -h ocalhost -p -u tom/ana
Enter password: cbpass

### 包含cookbook数据库的表备份
mysqldump -h localhost -p -u tom/ana mysqlcookbook >mysqlcookbook.sql
mysqldump -h localhost -p -u root students > students.sql

mysql -p -u root  test < students.sql
#### or
mysql> source  students.sql;
#### 管道
mysqldump -h localhost -p -u tom/ana mysqlcookbook | mysql  -h xyz.com -p -u root  test

mysqladmin -p -u root shutdown
```

### 2 查询结构生成xml或者html文档
```
mysql  -h localhost -p -u tom/ana -e "SELECT * FROM limits WHERE legs=0 " mysqlcookbook
mysql  -h localhost -p -u root  -e "SELECT * FROM transcripts " test

mysql  -h localhost -p -u tom/ana -H -e "SELECT * FROM limits WHERE legs=0 " mysqlcookbook
mysql  -h localhost -p -u root -X -e "SELECT * FROM transcripts " test  # -H --> --html

mysql  -h localhost -p -u tom/ana -X -e "SELECT * FROM limits WHERE legs=0 " mysqlcookbook
mysql  -h localhost -p -u root -X -e "SELECT * FROM transcripts " test # -X --> --xml
```


### 3 perl DBI
```
yum install perl-CPAN
perl -MCPAN -eshell
install DBI
# or
yum install perl-DBD-MySQL
# or
perl -MCPAN -e "install DBD::mysql"
# or
wget http://search.cpan.org/CPAN/authors/id/C/CA/CAPTTOFU/DBD-mysql-4.027.tar.gz
tar -xvzf /DBD-mysql-4.027.tar.gz
cd /DBD-mysql-4.027 && perl  Makefile.PL && make && make install
```

`connect.pl`

```
use strict;
use warning;
use DBI;

my $user = "root";
my $passwd = "123456";
my $host = "localhost";
my $database = "test";

my $dsn = "DBI:mysql:host=$host;database=$database ;";

my $dbh = DBI->connect($dsn,$user,$passwd) or die "Cannot connect to serve $host\n";
print "Connected\n";

$dbh->disconnect();
print "Disconnected\n";
```


### 4 python DB

```
sudo yum search mysqldb
#sudo yum install MySQL-python.x86_64
wget https://pypi.python.org/packages/2.6/s/setuptools/setuptools-0.6c11-py2.6.egg  --no-check-certificate
wget https://pypi.python.org/packages/source/p/pip/pip-1.3.1.tar.gz --no-check-certificate
pip install MySQLdb
### TODO 20140723
```

`connet.py`

```
# -*- coding: UTF-8 -*-
import sys
import MySQLdb

def main():
    try:
        connect = MySQLdb.connect(db = "test",
                        host = "localhost",
                        user = "root",
                        passwd = "123456")
        # Non-local TCP/IP 
        '''
        connect = MySQLdb.connect(db = "test",
                        host = "mysql.example.com",
                        port = 3307,
                        user = "root",
                        passwd = "123456")
        '''
        print "Connected"
    except :
        print "Can not connect to server"

if __name__ == '__main__':
    main()
```

```
SHOW FULL PROCESSLIST\g; # 当前运行状况

EXPLAIN SELECT * FROM city\G
SHOW TABLE STATUS like 'city'\G # 表city的信息


#EXPLAIN
EXPLAIN SELECT host,user,password FROM mysql.user\G

SHOW CREATE TABLE city\G 
SHOW INDEXES FROM city\G
SELECT COUNT(*) FROM city;

### innodb_buffer
SHOW GLOBAL STATUS LIKE  'innodb_buffer%';
SHOW ENGINE INNODB STATUS;


prompt = \\h/\\u:[\\d] >\\_
``` 
### TODO 20140723


