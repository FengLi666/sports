from login import *

mobile = input('input your account\n')
password = input('input your password\n')

try:
    userid, s = login(mobile, password)
except Exception as e:
    traceback.print_exc()
    print('login failed')
    exit(0)

print('loging successfully')

try:
    dis = input('input distance you need\n')
    no_free_run(userid, s, dis=float(dis))
except Exception as e:
    traceback.print_exc()
    print('run failed')
    exit(0)
input('run %s km successfully !\n'%dis)