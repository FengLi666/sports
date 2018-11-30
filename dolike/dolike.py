from gevent.monkey import patch_all

patch_all()
from gevent.pool import Pool

import traceback

from mysports.sports import get_md5_code
from mysports.original_json import *
from mysports.login import login
import requests
import json
import time


def dolike(ses: requests.session, to_userid: str, type: int = 1):
    data = json.dumps({"from": "1", "toUserId": to_userid, "type": str(type)})
    sign = get_md5_code(data)
    res = ses.post(host + '/api/center/doLike', data={'sign': sign, 'data': data})
    if res.json()['code'] != 200:
        print(res.text)
        raise Exception


if __name__ == '__main__':
    account = ''
    password = ''
    to_userid = '175691'
    try:
        print('try login...')
        _, s,_ = login(account, password)
    except Exception as e:
        traceback.print_exc()
        print('login failed')
        exit(0)

    print('loging successfully')

    try:
        pool = Pool(size=100)
        for i in range(500):
            pool.spawn(dolike, s, to_userid, 1)
            time.sleep(.05)
    except:
        traceback.print_exc()
