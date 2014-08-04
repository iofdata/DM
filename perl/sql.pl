## 	A 不返回结果
##	INSERT
##	DELETE
##	UPDATE
my $count = $dbh->("UPDATE profile SET cats = cats + 1 WHERE name = 'Fred' ");
if ($count) { # 如果发生错误则输出行数
    $count += 0; # 0E0
    print "Number of row updated: %d\n", $count;
}

## 	B 返回结果
##	SELECT
##	SHOW
##	EXPLAIN
##	DESCRIBE
##	1.首先,prepare()执行语句,
##		成功:	返回用于后续操作的statement句柄，
##		失败:	停止或返回undef
##	2.调用execute()执行语句，生成结果集
##	3.循环语句获取返回的行
##	4.finish() 释放资源

#1
my $sth = $dbh->prepare("SELECT id, name, cats FROM profile"); 
#2
$sth->execute();
my $count;
#3
# fetchrow_array()显示的定义select语句
# my $ref = $sth->fetchrow_arrayref()  通过$ref->[0]来访问
# my $ref = $sth->fetchrow_hashref()   通过$ref->{id}来访问，列名需唯一
while (my @val = $sth->fetchrow_array()) {
	print "id:$val[0], name:$val[1],cats:$val[2]\n";
	++$count;
}
#4
$sth->finish();
print "Number of rows returned: %d\n", $count;


##	数据库句柄方法
#	selectrow_array() 
#	selectrow_arrayref()
#	selectcol_arrayref()
#	selectall_arrayref()
#	selectrow_hashref()
#	selectall_hashref()
my @val = $dbh->selectrow_array("SELECT id, name, cats FROM profile WHERE id = 3"); 

