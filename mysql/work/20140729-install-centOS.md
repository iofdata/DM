#### A. 光盘重装系统
````
reboot(crtl+allt+delete) 
-> 
F2(system manage) 
-> 
F11(BIOS Menu) 
-> 
BIOS Boot Setting 
->
Boot Sequence 
-> 
COD(DVD or U Driver) 
-> 
OK 
-> 
Install from video 
-> 
No Test 
-> 
Basic 
-> 
Fresh 
-> 
Use All 
-> 
Basic Server 
-> 
reboot
```


#### B. 固定Ip上网设置
```
vim  /etc/sysconfig/network-scripts/ifcfg_ethm1

DEVICE="etho"
HWADDR="...."
BOOTPROTO="static" # changed to static
ONBOOT="yes"
IPADDR="59.175.153.94"
NETMASK="255.255.255.0"
GATEWAY="59.175.153.1"
DNS1="202.103.24.68"


chkconfig | grep network
service network restart
ping www.baidu.com
```