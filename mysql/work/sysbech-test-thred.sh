


host=localhost
port=3306
socket=/home/data/mysql/mysql.sock
user=root
password=123456

resultsdir=./results-thread

threads="8 16 32 64 128"

sizes="1000000 5000000 10000000 15000000 20000000 25000000 30000000"

mkdir -p $resultsdir

for thread in $threads;do
        mkdir $resultsdir/thread-$thread
        for size in $sizes; do
                sysbench --test=oltp --mysql-table-engine=innodb --oltp-table-size=$size --mysql-socket=$socket --mysql-user=$user --mysql-host=$host --mysql-password=$password --mysql-db=students --oltp-table-name=test$size prepare;
                sysbench --test=oltp --mysql-table-engine=innodb --oltp-table-size=$size --mysql-socket=$socket --mysql-user=$user --mysql-host=$host --mysql-password=$password --mysql-db=students --oltp-table-name=test$size  --max-requests=1000 --num-threads=$thread run | tee -a $resultsdir/thread-$thread/sysbench.$thread.$size.report;
                sysbench --test=oltp --mysql-host=$host  --mysql-user=$user --mysql-password=$password --mysql-socket=$socket --mysql-db=students --oltp-table-name=test$size  cleanup;
        done
done
