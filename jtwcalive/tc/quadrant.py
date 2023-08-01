"""
Four Quadrants of the wind radii
"""
from dataclasses import dataclass


@dataclass
class WindQuadrants:
    NE: int
    SE: int
    SW: int
    NW: int

    def __str__(self):
        return f"NE: {self.NE} SE: {self.SE} SW: {self.SW} NW: {self.NW}"

    @classmethod
    def from_str(cls, _str: str):
        """
        _src = '064 KT WINDS - 060 NM NORTHEAST QUADRANT
                            050 NM SOUTHEAST QUADRANT
                            050 NM SOUTHWEST QUADRANT
                            030 NM NORTHWEST QUADRANT'

        :param _str:
        :return: WindQuadrants
        """
        _str = _str.replace("KT WINDS - ", "")
        _str = _str.replace("NM", "")
        _str = _str.replace("QUADRANT", "")
        _str = _str.replace(" ", "")
        _str = _str.replace("\n", "")

        _list = _str.split()

        return cls(
            NE=int(_list[1]),
            SE=int(_list[2]),
            SW=int(_list[3]),
            NW=int(_list[4]),
        )
