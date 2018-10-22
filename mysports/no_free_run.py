import json
import random
from datetime import datetime, timedelta

from mysports.original_json import *
from mysports.sports import *
from path_plan.plan import path_plan, coord_trans


def no_free_run(userid: str, ses, dis: float = 2, start_point=gps_point(30.879521,121.892966)):
    data = json.dumps({"initLocation": "121.85284044053819,30.911461588541666", "type": "1", "userid": userid})

    res = ses.get(host + '/api/run/runPage', params={'sign': get_md5_code(data), 'data': data.encode('ascii')})

    resj = res.json()['data']

    x = {"buPin": "0.0", "duration": "1000",
         "endTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
         "startTime": (datetime.now() - timedelta(seconds=480)).strftime("%Y-%m-%d %H:%M:%S"),
         "frombp": "0", "goal": "2.00",
         "totalNum": "0",
         "trend": [], "type": "1",
         "userid": userid, 'real': str(dis * 1000), 'runPageId': resj['runPageId'], 'speed': "4'00''"
         }

    # gpl = gps_point_list()
    # gpl.run(start_point=start_point, stripe=0.001)

    # pass_by_ps = []

    #red, green
    red, green = 2, 4
    x['bNode'] = resj['ibeacon'][:red]
    x['tNode'] =  resj['gpsinfo'][:green]
    position_info = x['bNode'][0]['position']
    start_point = gps_point(float(position_info['latitude']), float(position_info['longitude']))
    start_point.zouzou(strip=0.005)
    pass_by_ps = [coord_trans(start_point.json)]
    # reformat bnode, tnode ;  collect passby points
    for node in x['bNode']:
        pos = node['position']
        pos['latitude'] = float(pos['latitude'])
        pos['longitude'] = float(pos['longitude'])
        pos['speed'] = 0.0
        node['position'] = pos
        str_coord = coord_trans(pos)
        pass_by_ps.append(str_coord)

    for pos in x['tNode']:
        pos['latitude'] = float(pos['latitude'])
        pos['longitude'] = float(pos['longitude'])
        pos['speed'] = 0.0
        str_coord = coord_trans(pos)
        pass_by_ps.append(str_coord)

    #path plan
    plan = path_plan(pass_by_ps)
    dis = plan['distance']
    path = plan['path']

    #reformat path
    tmp = []
    for p in path:
        tmp.append({'latitude':p['lat'], 'longitude':p['lng']})
    path = tmp

    # insert path, dis, duration, speed into x
    speed = random.randint(300, 500) # seconds per km
    duration = dis * speed  #seconds
    # to 'minutes'seconds'microseconds'
    speed = "%s'%s''"%(speed//60,speed - speed//60 * 60)
    startTime = (datetime.now() - timedelta(seconds=duration)).strftime("%Y-%m-%d %H:%M:%S")

    x['real'] = str(dis*1000)
    x['duration'] = str(duration)
    x['speed'] = speed
    x['track'] = path
    x['startTime'] = startTime

    xs = json.dumps(x)

    r = ses.post(host + '/api/run/saveRunV2', data={'sign': get_md5_code(xs), 'data': xs.encode('ascii')})
    print(r.content.decode('utf-8'))
    return dis