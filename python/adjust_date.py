from datetime import datetime
import time

def test(aa,bb):
	cc,dd = adjust_date(aa,bb)
	print aa,bb,cc,dd


def adjust_date(send_time,msg_time):
	date_str = msg_time.split()[0]
	stime = datetime.strptime(date_str  + " " + send_time, "%Y-%m-%d %H:%M:%S")
	rtime = datetime.strptime(msg_time, "%Y-%m-%d %H:%M:%S")
	if stime.hour == 0 and rtime.hour == 23:
		stime =  stime.replace(day = stime.day + 1 )
	if stime.hour < 6:
		rtime = datetime.strptime(date_str  + " 00:00:00" , "%Y-%m-%d %H:%M:%S")
	elif stime.hour < 12:
		rtime = datetime.strptime(date_str  + " 06:00:00" , "%Y-%m-%d %H:%M:%S")
	elif stime.hour < 18:
		rtime = datetime.strptime(date_str  + " 12:00:00" , "%Y-%m-%d %H:%M:%S")
	else:
		rtime = datetime.strptime(date_str  + " 18:00:00" , "%Y-%m-%d %H:%M:%S")
	return (stime,rtime)


def main():
	test("00:04:07","2015-04-19 23:51:41")
	test("01:04:07","2015-04-20 00:51:41")
	test("00:44:10","2015-04-21 00:31:41")
	test("23:15:01","2015-04-15 23:02:44")
	test("21:00:06","2015-03-12 20:49:12")

if __name__ == '__main__':
	main()
