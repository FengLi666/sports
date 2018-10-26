import json
import traceback
import uuid

import requests

from mysports.free_run import free_run
from mysports.no_free_run import no_free_run
from mysports.original_json import headers, host
from mysports.sports import get_md5_code


def login(mobile, psd):
    headers['uuid'] = uuid.uuid4().hex.upper()
    s = requests.Session()

    s.headers = headers

    # get cookie
    data = r'{}'
    s.get(host + '/api/configuration/apiConfig', params={'sign': get_md5_code(data), 'data': data})

    login_data = json.dumps(
        {"info": headers['uuid'], "mobile": str(mobile), "password": str(psd), "type": "HUAWEIMLA-AL10"})

    login_res = s.get(host + '/api/reg/login', params={'sign': get_md5_code(login_data), 'data': login_data})
    login_rd = login_res.json()

    userid = login_rd['data']['userid']
    utoken = login_rd['data']['utoken']

    s.headers.update({'utoken': utoken})
    return (userid, s)

if __name__=='__main__':

    try:
        userid, s = login('18616805603', '123qwe')
    except Exception as e:
        traceback.print_exc()
        print('login failed')

    print('loging successfully')
    type = input('not_free :0  free: 1\n')
    while type not in ('1','0'):
        print('1 or 0 please !!!')
        type = input('not_free :0  free: 1\n')
    type = int(type)
    while 1:
        x = input('distance or quit\n')
        if x=='quit':
            break;
        try:
            if type:
                free_run(userid, s, dis=float(x))
            else:
                no_free_run(userid, s, dis=float(x))
        except Exception as e:
            traceback.print_exc()
            print('something wrong, try again')

