import hashlib

from math import pi, sqrt, sin, cos, atan2


def haversine(pos1, pos2):
    try:
        lat1 = float(pos1['lat'])
    except:
        lat1 = float(pos1['latitude'])
    try:
        long1 = float(pos1['lng'])
    except:
        long1 = float(pos1['longitude'])
    try:
        lat2 = float(pos2['lat'])
    except:
        lat2 = float(pos2['latitude'])
    try:
        long2 = float(pos2['lng'])
    except:
        long2 = float(pos2['longitude'])

    degree_to_rad = float(pi / 180.0)

    d_lat = (lat2 - lat1) * degree_to_rad
    d_long = (long2 - long1) * degree_to_rad

    a = pow(sin(d_lat / 2), 2) + cos(lat1 * degree_to_rad) * cos(lat2 * degree_to_rad) * pow(sin(d_long / 2), 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    km = 6367 * c
    mi = 3956 * c

    return {"km": km, "miles": mi}


def get_md5_code(s):
    hl = hashlib.md5()
    hl.update(('lpKK*TJE8WaIg%93O0pfn0#xS0i3xE$z' + 'data' + s).encode('ascii'))
    return hl.hexdigest()


class gps_point:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def distance(self, ap):
        # todo
        # return geodesic((self.latitude, self.longitude), (ap.latitude, ap.longitude)).kilometers
        return 2

    def zouzou(self, strip=0.001):
        '''
        随便走走
        :param strip: 步长
        :return gps_point :
        '''
        import random
        import copy
        new = copy.copy(self)
        new.latitude += random.uniform(-strip, strip)
        new.longitude += random.uniform(-strip, strip)
        return new

    @property
    def json(self):
        return {"latitude": self.latitude, "longitude": self.longitude}

    def __str__(self):
        return '%s,%s' % (self.latitude, self.longitude)


class gps_point_list:
    def __init__(self, points=None):
        if points:
            self.p_list = points
        else:
            self.p_list = []

    def append(self, point):
        self.p_list.append(point)

    def run(self, start_point=gps_point(30.8669741312, 121.9183560969), num=10, stripe=0.001):
        self.append(start_point)
        curr_pos = start_point
        for i in range(num):
            new_pos = gps_point(curr_pos.latitude + stripe, curr_pos.longitude + stripe)
            self.append(new_pos)
            curr_pos = new_pos

    def get_str_list(self):
        return [str(x) for x in self.p_list]

    @property
    def total_distance(self):
        res = 0
        for i, point in enumerate(self.p_list[1:]):
            res += point.distance(self.p_list[i - 1])
        return res

    def get_speed(self, duration=20):
        return duration / 60 / self.total_distance

    def get_track(self):
        return [x.json for x in self.p_list]

    def get_random_supplement(self):
        # todo
        pass
