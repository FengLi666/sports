import urllib
import hashlib
import requests
import time
from typing import List, Dict

host = 'http://api.map.baidu.com'
my_ak = 'ZbSlyWlvsXVKYuoHYkKiOmdQsG462IIy'
my_sk = 'tvomES1GLg7w8N3rp2aoCXSoPHrQ28l0'


def get_sn(url: str):
    queryStr = url + '&ak=%s' % my_ak + '&timestamp=%s' % time.time()
    encodedStr = urllib.parse.quote(queryStr, safe="/:=&?#+!$,;'@()*[]")
    rawStr = encodedStr + my_sk
    sn = hashlib.md5(urllib.parse.quote_plus(rawStr).encode('ascii')).hexdigest()
    return queryStr + '&sn=%s' % sn


def url_params(url: str, params: Dict):
    l = []
    for k, v in params.items():
        l.append('%s=%s' % (k, v))
    return url + '&'.join(l)


def get_route(startp: str, endp: str, region='上海'):
    url = '/direction/v1?'
    oj = {
        'origin': startp,
        'destination': endp,
        'mode': 'walking',
        'region': region,
        'output': 'json',
    }
    r = requests.get(host + get_sn(url_params(url, oj)))
    rj = r.json()
    route = rj['result']['routes'][0]
    steps = route['steps']
    dis = route['distance'] / 1000
    path = [steps[i]['stepOriginLocation'] for i in range(len(steps))]
    return {'distance': dis, 'route': path}


def path_plan(points: List[str]) -> Dict:
    index = 0
    paths = []
    dis = 0
    while index < len(points) - 1:
        startp, endp = points[index], points[index + 1]

        route = get_route(startp, endp, region='上海')
        paths += route['route']
        dis += route['distance']

        index += 1
    return {'distance': dis, 'path': paths}

def coord_trans(p : dict):
    return '%s,%s'%(p['latitude'], p['longitude'])


if __name__ == '__main__':
    print(path_plan(['30.8859890000,121.8948540000', '30.8801380000,121.8937980000', '30.8795210000,121.8929660000']))

    print(get_route('30.8859890000,121.8948540000', '30.8801380000,121.8937980000'))