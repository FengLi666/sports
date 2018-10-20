import json
from datetime import datetime, timedelta
from sports import  *
from mysports.original_json import post_data


def gen_freerun_json(run_pid, dis=2, start_point=gps_point(30.8669741312, 121.9183560969)):
    data = post_data
    data['runPageId'] = run_pid
    data['type'] = 2
    gpl = gps_point_list()
    gpl.run(stripe=0.0001, start_point=start_point)
    data['real'] = dis * 1000
    data['duration'] = "1200"
    sp = (float(data['duration']) / 60) / (data['real'] / 1000)
    data['speed'] = "%d\u0027%d\u0027\u0027" % (int(sp), (sp - int(sp)) * 60)
    data['track'] = gpl.get_track()
    data['endTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data['startTime'] = (datetime.now() - timedelta(seconds=60 * 20)).strftime('%Y-%m-%d %H:%M:%S')
    print('try run %.2f km, speed=%s' % (data['real'] / 1000, data['speed']))
    return json.dumps(data)


def free_run(userid, ses, dis=1, start_point=gps_point(30.8669741312, 121.9183560969)):
    host = 'http://gxhttp.chinacloudapp.cn'

    init_data = json.dumps({"initLocation": "", "type": "2", "userid": userid})
    post_data['userid'] = userid

    sign = get_md5_code(init_data)
    res = ses.get(host + '/api/run/runPage',
                  params={'sign': sign, 'data': init_data.encode('ascii')})
    print(res.content.decode('utf-8'))
    resj = res.json()
    run_pid = resj['data']['runPageId']
    response_body = gen_freerun_json(run_pid, dis=dis, start_point=start_point)

    sign = get_md5_code(response_body)
    rep = ses.post(host + '/api/run/saveRunV2', data={'sign': sign, 'data': response_body.encode('ascii')}
                   )
    print(rep.content.decode('utf-8'))
