from mysports.login import *
from mysports.no_free_run import no_free_run
import traceback
import argparse


def run(account, password, rg=(2, 4), debug=False):
    try:
        print('try login...')
        userid, s, school = login(account, password)
    except Exception as e:
        traceback.print_exc()
        print('login failed')

    print('loging successfully')

    try:
        print('try run...')
        dis = no_free_run(userid, s, school=school, rg=rg, debug=debug)
        print('run %s km successfully !\n' % dis)
    except Exception as e:
        traceback.print_exc()
        print('run failed')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='take a no free run')
    parser.add_argument('--red', type=int, default=2, help='red points to reach,default = 2')
    parser.add_argument('--green', type=int, default=4, help='green points to reach,default = 4')
    parser.add_argument('--debug', type=bool, default=False,
                        help='--debug True will post the run immediately, and print debug info')
    args = parser.parse_args()
    mobile = input('input your account\n')
    password = input('input your password\n')
    run(mobile, password, rg=(args.red, args.green), debug=args.debug)
    input('press any key to quit...')
