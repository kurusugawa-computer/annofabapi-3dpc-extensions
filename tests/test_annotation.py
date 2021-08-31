import json
import os
from pathlib import Path

import annofabapi
from annofabapi.parser import SimpleAnnotationDirParser

from annofab_3dpc.annotation import (
    CuboidAnnotationDetailDataV2,
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


class TestAnnotation:
    @classmethod
    def setup_class(cls):
        with (data_dir / "simple_annotation.json").open() as f:
            dict_simple_annotation = json.load(f)

        cls.details = dict_simple_annotation["details"]

    def test_convert_annotation_detail_data_with_segment(self):
        detail = self.details[0]
        result = convert_annotation_detail_data(detail["data"])
        print(result)
        assert type(result) == SegmentAnnotationDetailData
        print(result.dump())
        assert result.dump() == detail["data"]

    def test_convert_annotation_detail_data_with_cuboid(self):
        detail = self.details[1]
        result = convert_annotation_detail_data(detail["data"])
        print(result)
        assert type(result) == CuboidAnnotationDetailDataV2
        print(result.dump())
        print(detail["data"])
        assert json.loads(result.dump()) == json.loads(detail["data"])

    def test_convert_annotation_detail_data_with_other(self):
        detail = self.details[2]
        result = convert_annotation_detail_data(detail["data"])
        print(result)
        assert type(result) == dict


def test_convert_annotation_detail_data():
    parser = SimpleAnnotationDirParser(data_dir / "simple_annotation.json")
    result = parser.parse(convert_annotation_detail_data)
    assert type(result.details[0].data) == SegmentAnnotationDetailData
    assert type(result.details[1].data) == CuboidAnnotationDetailDataV2
    assert type(result.details[2].data) == dict
