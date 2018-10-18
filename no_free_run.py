import json
from datetime import datetime, timedelta

from original_json import *
from sports import *


def no_free_run(userid: str, ses, dis: float = 2, start_point=gps_point(30.8669741312, 121.9183560969)):
    data = json.dumps({"initLocation": "121.85284044053819,30.911461588541666", "type": "1", "userid": userid})

    res = ses.get(host + '/api/run/runPage', params={'sign': get_md5_code(data), 'data': data.encode('ascii')})

    resj = res.json()['data']

    x = {"buPin": "0.0", "duration": "1000",
         "endTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
         "startTime": (datetime.now() - timedelta(seconds=480)).strftime("%Y-%m-%d %H:%M:%S"),
         "frombp": "0", "goal": "2.00",
         "totalNum": "0",
         "trend": [], "type": "1",
         "userid": userid, 'real': str(dis * 1000), 'runPageId': resj['runPageId'], 'speed': "4'00''",
         'bNode': resj['ibeacon'], 'tNode': resj['gpsinfo']}

    gpl = gps_point_list()
    gpl.run(start_point=start_point, stripe=0.0001)
    x['track'] = gpl.get_track()
    for node in x['bNode']:
        pos = node['position']
        pos['latitude'] = float(pos['latitude'])
        pos['longitude'] = float(pos['longitude'])
        pos['speed'] = 0.0
        node['position'] = pos
    for pos in x['tNode']:
        pos['latitude'] = float(pos['latitude'])
        pos['longitude'] = float(pos['longitude'])
        pos['speed'] = 0.0

    xs = json.dumps(x)

    r = ses.post(host + '/api/run/saveRunV2', data={'sign': get_md5_code(xs), 'data': xs.encode('ascii')})
    print(r.content.decode('utf-8'))
