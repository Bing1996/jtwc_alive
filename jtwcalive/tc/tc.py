from collections import UserList
from datetime import datetime

from .node import Node


class TC(UserList):
    """
    One TC object contains a list of Node objects.
    """

    create_node = Node

    def __init__(self, src: str, **kwargs):
        UserList.__init__(self)
        self.src = src

        # 如果为同一台风不同的NWP机构则需要获取tc_header
        for k, v in kwargs.items():
            setattr(self, k, v)

        # 记录额外参数
        self.__kwargs = kwargs

    @property
    def life_span(self):
        _time_list = self.to_list('time')
        _dt = _time_list[-1] - _time_list[0]

        return int(_dt.days * 24 + _dt.seconds // 3600)

    def to_list(self, _var: str) -> list:
        """
        获取不同的一维时间序列， 比如lat、lon、press等
        """
        return [getattr(node, _var) for node in sorted(self)]

    def __contains__(self, item: Node):
        if item.time not in self.to_list("time"):
            return False

        return True

    def append(self, item: Node) -> None:
        """
        判断需要不存在相同的时间点才能添加
        :param item:
        :return:
        """
        if not isinstance(item, Node):
            raise TypeError("only Node type can be appended!")

        if item in self:
            raise KeyError("Node existed!")

        UserList.append(self, item)

    def get_node(self, node_time: datetime) -> Node:
        for node in self:
            if node.time == node_time:
                return node

        raise KeyError(f"{node_time} is not existed!")

    @property
    def init_time(self) -> datetime:
        for node in sorted(self):
            return node.time

    @property
    def tc_rank(self) -> str:
        for node in sorted(self):
            return node.gr

    def to_dict(self):
        """
        标准化输出
        :return:
        """

        pass