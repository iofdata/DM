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