import hashlib
import time
import urllib
from typing import List, Dict
from mysports.sports import gps_point, gps_point_list

import requests

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
        'coord_type': 'gcj02',
        'ret_coordtype': 'gcj02'
    }
    r = requests.get(host + get_sn(url_params(url, oj)))
    rj = r.json()
    route = rj['result']['routes'][0]
    steps = route['steps']
    dis = route['distance'] / 1000
    spliter = lambda path: [
        {
            'lng': p.split(',')[0],
            'lat': p.split(',')[1]
        }
        for p in path.split(';')]
    path = [spliter(steps[i]['path']) for i in range(len(steps))]
    path = [item for lst in path for item in lst]
    return {'distance': dis, 'route': path}


def path_plan(points: gps_point_list) -> Dict:
    # to list of str
    points = points.get_str_list()

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


def gen_human_like_route(path: List[str]):
    # todo
    pass
