import json
import math
import os
from pathlib import Path

import pytest
from annofabapi.parser import SimpleAnnotationDirParser

from annofab_3dpc.annotation import (
    CuboidAnnotationDetailDataV2,
    EulerAnglesZXY,
    Location,
    SegmentAnnotationDetailData,
    convert_annotation_detail_data,
)

# プロジェクトトップに移動する
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/../")

data_dir = Path("./tests/data")


class TestLocation:
    def test_add(self):
        l1 = Location(1, 2, 3)
        l2 = Location(2, 3, 4)
        assert l1 + l2 == Location(3, 5, 7)

    def test_sub(self):
        l1 = Location(1, 2, 3)
        l2 = Location(5, 5, 5)
        assert l2 - l1 == Location(4, 3, 2)


class TestEulerAnglesZXY:
    def test_main(self):
        euler_angles = EulerAnglesZXY(0, math.pi / 2, 0)
        quaternion = euler_angles.to_quaternion()
        actual = EulerAnglesZXY.from_quaternion(quaternion)
        assert actual.x == pytest.approx(euler_angles.x)
        assert actual.y == pytest.approx(euler_angles.y)
        assert actual.z == pytest.approx(euler_angles.z)


class TestAnnotation:
    @classmethod
    def setup_class(cls):
        with (data_dir / "simple_annotation.json").open() as f:
            dict_simple_annotation = json.load(f)

        cls.details = dict_simple_annotation["details"]

    def test_convert_annotation_detail_data_with_segment(self):
        detail = self.details[0]
        result = convert_annotation_detail_data(detail["data"])
        assert type(result) == SegmentAnnotationDetailData
        assert result.dump() == detail["data"]

    def test_convert_annotation_detail_data_with_cuboid(self):
        detail = self.details[1]
        result = convert_annotation_detail_data(detail["data"])
        assert type(result) == CuboidAnnotationDetailDataV2

        assert json.loads(result.dump()["data"]) == json.loads(detail["data"]["data"])

    def test_convert_annotation_detail_data_with_other(self):
        detail = self.details[2]
        result = convert_annotation_detail_data(detail["data"])
        assert type(result) == dict


def test_convert_annotation_detail_data():
    parser = SimpleAnnotationDirParser(data_dir / "simple_annotation.json")
    result = parser.parse(convert_annotation_detail_data)
    assert type(result.details[0].data) == SegmentAnnotationDetailData
    assert type(result.details[1].data) == CuboidAnnotationDetailDataV2
    assert type(result.details[2].data) == dict
