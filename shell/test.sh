host=localhost
port=3306
socket=/home/data/mysql/mysql.sock
user=root
password=123456
resultsdir=./results
sizes="1000000 2000000 3000000 4000000 5000000 6000000 7000000 8000000 9000000 10000000 11000000 12000000 13000000 14000000 15000000 16000000 17000000 18000000 19000000 20000000"

mkdir -p $resultsdir

for size in $sizes; do
	sysbench --test=oltp --mysql-table-engine=innodb --oltp-table-size=$size --mysql-socket=$socket --mysql-user=$user --mysql-host=$host --mysql-password=$password --mysql-db=students --oltp-table-name=test$size prepare;
	sysbench --test=oltp --mysql-table-engine=innodb --oltp-table-size=$size --mysql-socket=$socket --mysql-user=$user --mysql-host=$host --mysql-password=$password --mysql-db=students --oltp-table-name=test$size  --max-requests=1000 --num-threads=10 run | tee -a $resultsdir/sysbench.$size.report;
	sysbench --test=oltp --mysql-host=$host  --mysql-user=$user --mysql-password=$password --mysql-socket=$socket --mysql-db=students --oltp-table-name=test$size  cleanup;
done