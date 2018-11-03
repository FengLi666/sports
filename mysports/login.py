import json
import uuid

import requests

from mysports.original_json import headers, host
from mysports.sports import get_md5_code


def login(mobile, psd):
    headers['uuid'] = uuid.uuid4().hex.upper()
    s = requests.Session()

    s.headers = headers

    # get cookie
    data = r'{}'
    s.get(host + '/api/configuration/ n', params={'sign': get_md5_code(data), 'data': data})

    login_data = json.dumps(
        {"info": headers['uuid'], "mobile": str(mobile), "password": str(psd), "type": "HUAWEIMLA-AL10"})

    login_res = s.get(host + '/api/reg/login', params={'sign': get_md5_code(login_data), 'data': login_data})
    login_rd = login_res.json()

    try:
        userid = login_rd['data']['userid']
        utoken = login_rd['data']['utoken']
    except:
        print(login_rd)
        raise Exception

    s.headers.update({'utoken': utoken})
    return userid, s
