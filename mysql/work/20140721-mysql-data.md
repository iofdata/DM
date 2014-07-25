新建1核1G主机-> jd-th-test01 (CentOS6.05)
200G硬盘
私有网络 192.168.2.27
root -> Mdjd2014

路由ip 
ssh root@121.201.7.185 //端口252
Whuxcl2014

私有主机
ssh root@192.168.2.27
Mdjd2014


fdisk /dev/sdc
mkfs.ext4 /dev/sdc1P
e2label /dev/sdc1 /home1

vi /etc/fstab
} -> a
LABEL=/home1            /home                   ext4    defaults        0 0

reboot

ssh root@192.168.2.27

### 安装MySQL
```
wget http://192.168.2.2:8080/download/MySQL-client-5.6.19-1.el6.x86_64.rpm
wget http://192.168.2.2:8080/download/MySQL-server-5.6.19-1.el6.x86_64.rpm
#wget -c http://dev.mysql.com/get/Downloads/MySQL-5.6/MySQL-devel-5.6.19-1.el6.x86_64.rpm/from/http://mysql.spd.co.il/

rpm -ivg MySQL-server-5.6.19-1.el6.x86_64.rpm
# 报错 
#file /usr/share/mysql/czech/errmsg.sys from install of MySQL-server-5.6.19-1.el6.x86_64 conflicts with file from package mysql-libs-5.1.71-1.el6.x86_64
 
yum remove mysql-libs-5.1.*
rpm -ivh MySQL-server-5.6.19-1.el6.x86_64.rpm

rpm -ivg MySQL-client-5.6.19-1.el6.x86_64.rpm

chkconfig
service mysql start

# 数据目录
lsof|grep mysql
ll -rt /var/lib/mysql/   

# mysql #配置文件
ll -rt /usr/share/mysql/

#相关程序命令
which mysql 
/usr/bin/mysql

#启动脚本
ll -rt /etc/rc.d/init.d/
```

### 切换mysql目录到 /home/data
```
#### 参见 http://database.51cto.com/art/200709/56715.htm 
mkdir /home/data
mysqladmin -u root -p shutdown # 关掉mysql服务
cd /home/data

lsof|grep mysql
ll -rt /var/lib/mysql # mysql 数据目录
mv /var/lib/mysql ./

##### 编辑MySQL的配置文件/etc/my.cnf
find / -name *.cnf -print 
    /home/data/mysql/auto.cnf
    /usr/share/doc/MySQL-server-5.6.19/my-default.cnf
    /usr/share/mysql/my-default.cnf
    /usr/my.cnf
    /etc/pki/tls/openssl.cnf
cp  /usr/my.cnf /etc/my.cnf
vi   /etc/my.cnf
#port    =   3306
socket  =   /home/data/mysql/mysql.sock
# 注释掉最后一行
##### 修改MySQL启动脚本/etc/init.d/mysql
vi　/etc/init.d/mysql
#datadir=/var/lib/mysql(注释此行)
datadir=/home/data/mysql (加上此行)
##### reboot
/etc/init.d/mysql restart 

##### error
ln -s  /home/data/mysql/mysql.sock /var/lib/mysql/
```


### mysql 报错  root@localhost 不能启动的问题
```
mysql -u root -p
Enter password: 
ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: YES)

service mysql stop
chkconfig
mysqld_safe --skip-grant-table

# http://wenku.baidu.com/link?url=ARPOWYE5qWssO6toplKyOFWoaVP57UeA3Lj3IUU00wk3tcP3EGpfEp52uJE8M_Ckio7sieL-8x0gOQ4Epwn8d4eUw_xpMNlGZZeswiPsg93
/etc/init.d/mysql stop 
mysqld_safe --user=mysql --skip-grant-tables --skip-networking &
mysql -u root mysql 
#mysql> UPDATE user SET Password='tanhao'  where USER='root';
mysql>   update mysql.user set password=password('tanhao') where user='root';
#mysql> select * FROM user WHERE USER='root'\G
mysql>SELECT host,user,password FROM user;
mysql> FLUSH PRIVILEGES;
mysql> quit
/etc/init.d/mysql restart 
mysql -uroot -p 
# You must SET PASSWORD before executing this statement解决
mysql> SET PASSWORD = PASSWORD('123456'); # new root key will be 123456
```

###  sysbench 安装
```
http://blog.163.com/digoal@126/blog/static/16387704020134142151769/

# 找不到mysql的include 和lib文件目录
wget -c http://dev.mysql.com/get/Downloads/MySQL-5.6/MySQL-devel-5.6.19-1.el6.x86_64.rpm/from/http://mysql.spd.co.il/
rpm -ivh MySQL-devel-5.6.19-1.el6.x86_64.rpm

wget -c http://dev.mysql.com/get/Downloads/MySQL-5.6/MySQL-shared-5.6.19-1.el6.x86_64.rpm/from/http://mysql.spd.co.il/
rpm -ivh MySQL-shared-5.6.19-1.el6.x86_64.rpm

rpm -qa|grep MySQL
rpm -ql MySQL-server-5.6.19-1.el6.x86_64

chkconfig --list|grep -i mysql

./configure --with-mysql-includes=/usr/include/mysql --with-mysql-libs=/usr/lib64/mysql/
make
make check
make install
```

### 最终解决方案
```
## 5。0 版本但是不能测试 oltp
http://www.lefred.be/node/154
rpm -ivh sysbench-0.5-2.el6_.x86_64.rpm
rpm -ql sysbench

#git clone https://github.com/nettedfish/sysbench_from_percona.git

## 转回 4.10 版本 解决方案
yum -y install libtool
yum -y install automake*
rm -rf libtool
ln -s /usr/bin/libtool ./
./autogen.sh
./configure 
make & make install
ln -s  /usr/local/bin/sysbench /usr/bin/ 
sysbench --test=oltp help

sysbench 0.4.10:  multi-threaded system evaluation benchmark

oltp options:
  --oltp-test-mode=STRING         test type to use {simple,complex,nontrx,sp} [complex]
  --oltp-sp-name=STRING           name of store procedure to call in SP test mode []
  --oltp-read-only=[on|off]       generate only 'read' queries (do not modify database) [off]
  --oltp-skip-trx=[on|off]        skip BEGIN/COMMIT statements [off]
  --oltp-range-size=N             range size for range queries [100]
  --oltp-point-selects=N          number of point selects [10]
  --oltp-simple-ranges=N          number of simple ranges [1]
  --oltp-sum-ranges=N             number of sum ranges [1]
  --oltp-order-ranges=N           number of ordered ranges [1]
  --oltp-distinct-ranges=N        number of distinct ranges [1]
  --oltp-index-updates=N          number of index update [1]
  --oltp-non-index-updates=N      number of non-index updates [1]
  --oltp-nontrx-mode=STRING       mode for non-transactional test {select, update_key, update_nokey, insert, delete} [select]
  --oltp-auto-inc=[on|off]        whether AUTO_INCREMENT (or equivalent) should be used on id column [on]
  --oltp-connect-delay=N          time in microseconds to sleep after connection to database [10000]
  --oltp-user-delay-min=N         minimum time in microseconds to sleep after each request [0]
  --oltp-user-delay-max=N         maximum time in microseconds to sleep after each request [0]
  --oltp-table-name=STRING        name of test table [sbtest]
  --oltp-table-size=N             number of records in test table [10000]
  --oltp-dist-type=STRING         random numbers distribution {uniform,gaussian,special} [special]
  --oltp-dist-iter=N              number of iterations used for numbers generation [12]
  --oltp-dist-pct=N               percentage of values to be treated as 'special' (for special distribution) [1]
  --oltp-dist-res=N               percentage of 'special' values to use (for special distribution) [75]

General database options:

  --db-driver=STRING  specifies database driver to use ('help' to get list of available drivers)
  --db-ps-mode=STRING prepared statements usage mode {auto, disable} [auto]


Compiled-in database drivers:
  mysql - MySQL driver

mysql options:
  --mysql-host=[LIST,...]       MySQL server host [localhost]
  --mysql-port=N                MySQL server port [3306]
  --mysql-socket=STRING         MySQL socket
  --mysql-user=STRING           MySQL user [sbtest]
  --mysql-password=STRING       MySQL password []
  --mysql-db=STRING             MySQL database name [sbtest]
  --mysql-table-engine=STRING   storage engine to use for the test table {myisam,innodb,bdb,heap,ndbcluster,federated} [innodb]
  --mysql-engine-trx=STRING     whether storage engine used is transactional or not {yes,no,auto} [auto]
  --mysql-ssl=[on|off]          use SSL connections, if available in the client library [off]
  --myisam-max-rows=N           max-rows parameter for MyISAM tables [1000000]
  --mysql-create-options=STRING additional options passed to CREATE TABLE []


###  关于libtool 错误的其它参考
http://wenku.baidu.com/link?url=DGlHEoWxiLWq4829Qp_7ngYB9r3glfkk_JOHEVNDedUWDSWJxYRPiv55KWkhSPnkeKPXjn2O2N6n-Xgqi_j4c2j2GIRfqU66l2NlWZ0mHSK

```


