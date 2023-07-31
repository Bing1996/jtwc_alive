from collections import UserDict

from .tc import TC


class EnsembleTracks(UserDict):
    """
    Container to hold multi TC objects
    """
    create_tc = TC

    @property
    def max_range(self) -> int:
        """
        搜寻最大长度的台风预报
        :return:
        """
        _max_length = 0

        for _, tc in self.items():
            if _max_length < len(tc):
                _max_length = len(tc)

        return _max_length

    def __init__(self, **kwargs):
        UserDict.__init__(self)

        for k, v in kwargs.items():
            setattr(self, k, v)

    def __setitem__(self, key: str, value: TC):
        """
        只有不存在在相同台风源才能添加
        :param key: 台风的唯一性标志，可表示为不同机构名，也可以是smg id
        :param value:
        :return:
        """

        if not isinstance(value, TC):
            raise TypeError("Only TC class type can be added!")

        if key in self:
            raise KeyError(f"{key} is existed")

        self.data[key] = value

    def to_dict(self) -> list:
        return [tc.to_dict() for _, tc in self.items()]

    def interpolation(self, interpolation_interval=15):
        """
        将每一条在集合中的台风进行插值
        """
        for _, tc in self.items():
            tc.interpolation(interpolation_interval=interpolation_interval)
