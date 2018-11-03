from mysports.login import *
from mysports.no_free_run import no_free_run
import traceback
import sys

def run(account, password, rg=(2, 4), debug=False):
    try:
        print('try login...')
        userid, s = login(account, password)
    except Exception as e:
        traceback.print_exc()
        print('login failed')

    print('loging successfully')

    try:
        print('try run...')
        dis = no_free_run(userid, s, rg=rg, debug=debug)
        print('run %s km successfully !\n' % dis)
    except Exception as e:
        traceback.print_exc()
        print('run failed')


if __name__ == '__main__':
    mobile = input('input your account\n')
    password = input('input your password\n')
    debug = False
    if len(sys.argv) == 3 and sys.argv[2] == 'debug':
        debug = True
    run(mobile, password, debug=debug)
    input('press any key to quit...')
