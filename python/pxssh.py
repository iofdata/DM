import pxssh  
import getpass  

try: 
    s = pxssh.pxssh() 
    hostname = raw_input('hostname: ')  
    username = raw_input('username: ')  
    password = getpass.getpass('password: ')  
    s.login (hostname, username, password)  
    s.sendline ('uptime')  # run a command  
    s.prompt()             # match the prompt  
    print s.before         # print everything before the propt.  
    s.sendline ('ls -l')  
    s.prompt() 
    print s.before  
    s.sendline ('df')  
<<<<<<< HEAD
    s.prompt() 
=======
    s.)prompt() 
>>>>>>> origin/master
    print s.before  
    s.logout() 
except pxssh.ExceptionPxssh, e:  
    print "pxssh failed on login." 
<<<<<<< HEAD
    print str(e)
=======
    print str(e)
>>>>>>> origin/master
