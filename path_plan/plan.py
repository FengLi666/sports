import hashlib
import random
import time
import urllib
from typing import List, Dict

import requests

from mysports.sports import gps_point_list, haversine

host = 'http://api.map.baidu.com'
my_ak = 'zqZrWc3iKoMsMRmUjrQyzneeWhIPxGvV'
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
    try:
        route = rj['result']['routes'][0]
    except:
        print("使用人数太多，百度地图api配额超限！")
        exit(0)
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

    paths = gen_human_like_route(paths)
    return {'distance': dis, 'path': paths}


def gen_human_like_route(path: List[dict]) -> List[dict]:
    '''

    :param path: ['lat': str, 'lng': str]
    :return: ['lat': str, 'lng': str]
    '''
    extra_points = []
    for i in range(len(path) - 1):
        points = []
        start_lng = float(path[i]['lng'])
        start_lat = float(path[i]['lat'])
        end_lng = float(path[i + 1]['lng'])
        end_lat = float(path[i + 1]['lat'])
        distance = haversine(path[i], path[i + 1])
        if distance['km'] > 0.02:
            extra_points_num = int(distance['km'] / 0.01)
            offset_lng = (end_lng - start_lng) / extra_points_num
            offset_lat = (end_lat - start_lat) / extra_points_num
            for j in range(extra_points_num):
                pos_lng = start_lng + offset_lng * j + random.uniform(-offset_lng,offset_lng)
                pos_lat = start_lat + offset_lat * j + random.uniform(-offset_lat,offset_lat)
                points.append(
                    {
                        'lng': str(pos_lng),
                        'lat': str(pos_lat)
                    }
                )
        extra_points.append(points)
    result_path = []
    for i in range(len(path) - 1):
        result_path.append(path[i])
        result_path.extend(extra_points[i])
        result_path.append(path[i + 1])
    return result_path
