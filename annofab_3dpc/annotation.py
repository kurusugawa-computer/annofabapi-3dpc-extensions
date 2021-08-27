import json
import math
from dataclasses import dataclass
from typing import Any, Dict, List

from dataclasses_json import DataClassJsonMixin

ANNOTATION_TYPE_UNKNOWN = "Unknown"


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

    def to_quaterion(self) -> List[float]:
        """
        クォータニオンを生成する。

        以下のサイトから移植
        https://github.com/BabylonJS/Babylon.js/blob/40ded9ccf1e1bd8ac9cdf3a26909d3e12bc60ab8/src/Maths/math.vector.ts#L3259-L3275
        https://github.com/BabylonJS/Babylon.js/blob/40ded9ccf1e1bd8ac9cdf3a26909d3e12bc60ab8/src/Maths/math.vector.ts#L3198-L3201

        Returns:
            クォータニオン[w,x,y,z]
        """
        yaw = self.y
        pitch = self.x
        roll = self.z

        halfRoll = roll * 0.5
        halfPitch = pitch * 0.5
        halfYaw = yaw * 0.5

        sinRoll = math.sin(halfRoll)
        cosRoll = math.cos(halfRoll)
        sinPitch = math.sin(halfPitch)
        cosPitch = math.cos(halfPitch)
        sinYaw = math.sin(halfYaw)
        cosYaw = math.cos(halfYaw)

        qx = (cosYaw * sinPitch * cosRoll) + (sinYaw * cosPitch * sinRoll)
        qy = (sinYaw * cosPitch * cosRoll) - (cosYaw * sinPitch * sinRoll)
        qz = (cosYaw * cosPitch * sinRoll) - (sinYaw * sinPitch * cosRoll)
        qw = (cosYaw * cosPitch * cosRoll) + (sinYaw * sinPitch * sinRoll)
        return [qw, qx, qy, qz]

    @classmethod
    def from_quaterion(cls, quaterion: List[float]) -> "EulerAnglesZXY":
        """
        quaterion から生成する。以下のコードを移植した。
        https://github.com/BabylonJS/Babylon.js/blob/40ded9ccf1e1bd8ac9cdf3a26909d3e12bc60ab8/src/Maths/math.vector.ts#L2970-L3001

        Args:
            quaterion: wxyzの1次元配列
        """
        qw = quaterion[0]
        qx = quaterion[1]
        qy = quaterion[2]
        qz = quaterion[3]

        sqx = qx * qx
        sqy = qy * qy
        sqz = qz * qz
        sqw = qw * qw

        zAxisY = qy * qz - qx * qw
        limit = 0.4999999

        if zAxisY < -limit:
            euler_y = 2 * math.atan2(qy, qw)
            euler_x = math.pi / 2
            euler_z = 0.0
        elif zAxisY > limit:
            euler_y = 2 * math.atan2(qy, qw)
            euler_x = -math.pi / 2
            euler_z = 0.0
        else:
            euler_z = math.atan2(2.0 * (qx * qy + qz * qw), (-sqz - sqx + sqy + sqw))
            euler_x = math.asin(-2.0 * (qz * qy - qx * qw))
            euler_y = math.atan2(2.0 * (qz * qx + qy * qw), (sqz - sqx - sqy + sqw))

        return cls(euler_x, euler_y, euler_z)


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

    def dump(self) -> Dict[str, Any]:
        """SimpleAnnotationDetailクラスのdataプロパティに対応するdictを生成する。"""
        tmp = self.to_dict()
        # keyの順番を3dpc editorに合わせる
        str_data = json.dumps(
            {"kind": tmp["kind"], "shape": tmp["shape"], "version": tmp["version"]}, separators=(",", ":")
        )
        return {"data": str_data, "_type": ANNOTATION_TYPE_UNKNOWN}


@dataclass
class SegmentAnnotationDetailData(DataClassJsonMixin):
    data_uri: str

    def dump(self) -> Dict[str, Any]:
        """SimpleAnnotationDetailクラスのdataプロパティに対応するdictを生成する。"""
        return {"data": self.data_uri, "_type": ANNOTATION_TYPE_UNKNOWN}


def convert_annotation_detail_data(dict_data: Dict[str, Any]) -> Any:
    """
    SimpleAnnotationDetailクラスのdict型であるdataプロパティを、3DPC Editor用のDataclassに変換します。
    3DPC Editor用のDataclassに変換できない場合は、引数をそのまま返します。

    Args:
        dict_data: SimpleAnnotationDetailクラスのdict型のdataプロパティ

    Returns:
        3DPC Editor用のDataclass
    """
    if dict_data["_type"] != ANNOTATION_TYPE_UNKNOWN:
        return dict_data
    try:
        tmp = json.loads(dict_data["data"])
        if isinstance(tmp, dict) and tmp.get("kind") == "CUBOID":
            return CuboidAnnotationDetailData.from_dict(tmp)
        else:
            return dict_data
    except json.JSONDecodeError:
        return SegmentAnnotationDetailData(dict_data["data"])
