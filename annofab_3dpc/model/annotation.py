from dataclasses import dataclass

from dataclasses_json import DataClassJsonMixin


@dataclass
class Location(DataClassJsonMixin):
    x: float
    y: float
    z: float

    def __add__(self, other):
        return self.__class__(
            x=self.x + other.x,
            y=self.y + other.y,
            z=self.z + other.z,
        )

    def __sub__(self, other):
        return self.__class__(
            x=self.x - other.x,
            y=self.y - other.y,
            z=self.z - other.z,
        )


@dataclass
class Vector3(DataClassJsonMixin):
    x: float
    y: float
    z: float


@dataclass
class EulerAnglesZXY(DataClassJsonMixin):
    """
     z-x-y系のオイラー角。単位はラジアン。
    """
    x: float
    y: float
    z: float




@dataclass
class Size(DataClassJsonMixin):
    width: float
    """cuboid座標系のY軸方向の長さ"""
    height: float
    """cuboid座標系のZ軸方向の長さ"""
    depth: float
    """cuboid座標系のX軸方向の長さ"""



@dataclass
class CuboidDirection(DataClassJsonMixin):
    """
    cuboidの向き（長さ1のベクトル）
    """
    front: Vector3
    """cuboid座標系X軸の正の方向"""
    up: Vector3
    """cuboid座標系Z軸の正の方向"""

    @staticmethod
    def from_rotation():
        pass


@dataclass
class CuboidShape(DataClassJsonMixin):
    dimensions: Size
    location: Location
    """cuboidの中心位置"""
    rotation: EulerAnglesZXY
    """cuboidの回転"""
    direction: CuboidDirection
    """cuboidの向き（cuboidの回転から一意に決まる）"""


@dataclass
class CuboidAnnotationDetailData(DataClassJsonMixin):
    shape: CuboidShape
    kind: str = "CUBOID"
    version: str = "2"


