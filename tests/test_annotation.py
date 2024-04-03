import json
import math
import os
from pathlib import Path

import pytest
from annofabapi.parser import SimpleAnnotationDirParser

from annofab_3dpc.annotation import (
    CuboidAnnotationDecodeError,
    CuboidAnnotationDetailDataV1,
    CuboidAnnotationDetailDataV2,
    CuboidDirection,
    EulerAnglesZXY,
    Location,
    SegmentAnnotationDetailData,
    SegmentData,
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


class TestCuboidDirection:
    def test_from_euler_angles(self):
        actual0 = CuboidDirection.from_euler_angles(EulerAnglesZXY(0, 0, 0))
        assert actual0.front.x == pytest.approx(1)
        assert actual0.front.y == pytest.approx(0)
        assert actual0.front.z == pytest.approx(0)
        assert actual0.up.x == pytest.approx(0)
        assert actual0.up.y == pytest.approx(0)
        assert actual0.up.z == pytest.approx(1)

        actual1 = CuboidDirection.from_euler_angles(
            EulerAnglesZXY(
                0,
                0,
                math.pi / 4,
            )
        )
        assert actual1.front.x == pytest.approx(math.sqrt(2) / 2)
        assert actual1.front.y == pytest.approx(math.sqrt(2) / 2)
        assert actual1.front.z == pytest.approx(0)
        assert actual1.up.x == pytest.approx(0)
        assert actual1.up.y == pytest.approx(0)
        assert actual1.up.z == pytest.approx(1)

        actual2 = CuboidDirection.from_euler_angles(EulerAnglesZXY(math.pi / 2, 0, 0))
        assert actual2.front.x == pytest.approx(1)
        assert actual2.front.y == pytest.approx(0)
        assert actual2.front.z == pytest.approx(0)
        assert actual2.up.x == pytest.approx(0)
        assert actual2.up.y == pytest.approx(-1)
        assert actual2.up.z == pytest.approx(0)

    def test_from_quaternion(self):
        actual0 = CuboidDirection.from_quaternion([1, 0, 0, 0])
        assert actual0.front.x == pytest.approx(1)
        assert actual0.front.y == pytest.approx(0)
        assert actual0.front.z == pytest.approx(0)
        assert actual0.up.x == pytest.approx(0)
        assert actual0.up.y == pytest.approx(0)
        assert actual0.up.z == pytest.approx(1)


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

    def test_convert_annotation_detail_data_with_cuboid_v1(self):
        detail = self.details[2]
        result = convert_annotation_detail_data(detail["data"])
        print(result)
        assert type(result) == CuboidAnnotationDetailDataV1

    def test_convert_annotation_detail_data_with_other(self):
        detail = self.details[3]
        result = convert_annotation_detail_data(detail["data"])
        assert type(result) == dict  # noqa: E721

    def test_raise_CuboidAnnotationDecodEerror(self):
        with (data_dir / "invalid_simple_annotation.json").open() as f:
            dict_simple_annotation = json.load(f)

        detail = dict_simple_annotation["details"][0]
        with pytest.raises(CuboidAnnotationDecodeError):
            convert_annotation_detail_data(detail["data"])


class TestSegmentaData:
    def test_main(self):
        parser = SimpleAnnotationDirParser(data_dir / "task1/input1.json")
        simple_annotation = parser.parse(convert_annotation_detail_data)

        segment_detail = simple_annotation.details[0]

        with parser.open_outer_file(Path(segment_detail.data.data_uri).name) as f:
            dict_segmenta_data = json.load(f)
            segment_data = SegmentData.from_dict(dict_segmenta_data)
            assert type(segment_data) == SegmentData
            assert len(segment_data.points) > 0


def test_convert_annotation_detail_data():
    parser = SimpleAnnotationDirParser(data_dir / "simple_annotation.json")
    result = parser.parse(convert_annotation_detail_data)
    assert type(result.details[0].data) == SegmentAnnotationDetailData
    assert type(result.details[1].data) == CuboidAnnotationDetailDataV2
    assert type(result.details[2].data) == CuboidAnnotationDetailDataV1
    assert type(result.details[3].data) == dict  # noqa: E721
