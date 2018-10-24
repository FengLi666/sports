import hashlib


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

    def zouzou(self,strip=0.001):
        '''
        随便走走
        :param strip: 步长
        :return gps_point :
        '''
        import random
        import copy
        new = copy.copy(self)
        new.latitude +=  random.uniform(-strip, strip)
        new.longitude += random.uniform(-strip, strip)
        return new

    @property
    def json(self):
        return {"latitude":self.latitude, "longitude": self.longitude}


class gps_point_list:
    def __init__(self):
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