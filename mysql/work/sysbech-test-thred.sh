host=localhost
port=3306
socket=/home/data/mysql/mysql.sock
user=root
password=123456

resultsdir=./results-thread

threads="8 16 32 64 128"

sizes="1000000 5000000 10000000 15000000 20000000 25000000 30000000"


printf "sizes,threads,transactions,trns p/s,deadlocks,dls p/s,read/write requests,r/w reqs p/s,min,avg,max,99 percentile \n" >> stat.txt

mkdir -p $resultsdir

for thread in $threads;do
        mkdir $resultsdir/thread-$thread
        for size in $sizes; do
        	sysbench --test=oltp --mysql-table-engine=innodb --oltp-table-size=$size  --mysql-socket=$socket --mysql-user=$user --mysql-host=$host --mysql-password=$password --mysql-db=students --oltp-table-name=test$size prepare;
             sysbench --test=oltp --mysql-table-engine=innodb --oltp-table-size=$size --mysql-socket=$socket --mysql-user=$user --mysql-host=$host --mysql-password=$password --mysql-db=students --oltp-table-name=test$size  --max-requests=1000 --num-threads=$thread run | tee -a $resultsdir/thread-$thread/sysbench.$thread.$size.report;
             sysbench --test=oltp --mysql-host=$host  --mysql-user=$user --mysql-password=$password --mysql-socket=$socket --mysql-db=students --oltp-table-name=test$size  cleanup;
             
             cat $resultsdir/thread-$thread/sysbench.$thread.$size.report | \
  	egrep " cat|threads:|transactions:|deadlocks|read/write|min:|avg:|max:|percentile:" | \
	sed  -e '1 s/Number of threads: //' | \
	tr -d "\n" | \
	sed -e 's/Number of threads: /\n/g' \
	-e 's/[A-Za-z\/]\{1,\}://g' \
	-e 's/read\/write//g' \
	-e 's/approx\.  95//g' \
	-e 's/per sec.)//g' \
	-e 's/ms//g' \
	-e 's/(//g'  \
	-e 's/  */,/g' | awk -v d=$size '{$0=d","$0}1' >> stat.txt
       
        done
done
