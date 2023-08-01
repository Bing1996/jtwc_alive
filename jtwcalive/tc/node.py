"""
台风节点模型
"""
from datetime import datetime
import bisect


class Node:
    """
    Node Model
    """

    def __init__(self, _time: datetime, lat, lon, ws, **kwargs):
        self.time = _time
        self.lat = lat
        self.lon = lon
        self.ws = ws

        for k, v in kwargs.items():
            setattr(self, k, v)

    def __lt__(self, other):
        return self.time < other.time

    @property
    def gr(self) -> str:
        """
        the grade of typhoon
        :return:
        """

        _ws = [12, 18, 25, 33, 41, 51]
        _rank = ["LPA", "TD", "TS", "STS", "TY", "STY", "SuTY"]

        try:
            gr = _rank[bisect.bisect(_ws, self.ws)]
        except IndexError:
            return "NA"
        except TypeError:
            return "NA"
        else:
            return gr

    @property
    def gr_number(self) -> int:
        """
        get the tc grand number
        :return:
        """

        _rank = ["LPA", "TD", "TS", "STS", "TY", "STY", "SuTY"]

        try:
            return _rank.index(self.gr)
        except ValueError:
            return -1

    @classmethod
    def parse_from_dict(cls, _dict: dict):
        mandatory_keys = ["time", "lat", "lon", "pres", "ws"]

        if all(key in _dict for key in mandatory_keys):
            return cls(
                _dict["time"],
                _dict["lat"],
                _dict["lon"],
                _dict["pres"],
                _dict["ws"],
            )
        else:
            raise KeyError("miss some key in Node init")

    def to_dict(self):
        self.__none_convert()

        # 判断受否含有is_origin属性
        # is_stock 代表从数据库未插值的原始点

        if hasattr(self, "is_origin"):
            return {
                "forecast_time": datetime.strftime(self.time, '%Y-%m-%dT%H:%M:%SZ'),
                "lo": self.lon,
                "la": self.lat,
                "press": self.pres,
                "windSpeed": self.ws,
                "gr": self.gr,
                "is_origin": self.is_origin
            }

        return {
            "forecast_time": datetime.strftime(self.time, '%Y-%m-%dT%H:%M:%SZ'),
            "lo": self.lon,
            "la": self.lat,
            "press": self.pres,
            "windSpeed": self.ws,
            "gr": self.gr,
        }

    def __none_convert(self):
        _check = ["lat", "lon", "pres", "ws"]

        for key in _check:
            _tmp = getattr(self, key)
            try:
                setattr(self, key, round(_tmp, 3))
            except TypeError:
                setattr(self, key, "-")