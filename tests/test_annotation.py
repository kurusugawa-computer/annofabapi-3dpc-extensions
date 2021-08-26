import json
import os
from pathlib import Path

from annofab_3dpc.annotation import (
    CuboidAnnotationDetailData,
    SegmentAnnotationDetailData,
    convert_annotation_deitail_data,
)

# プロジェクトトップに移動する
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/../")

data_dir = Path("./tests/data")


class TestAnnotation:
    @classmethod
    def setup_class(cls):
        with (data_dir / "simple_annotation.json").open() as f:
            dict_simple_annotation = json.load(f)

        cls.details = dict_simple_annotation["details"]

    def test_convert_annotation_deitail_data_with_segment(self):
        detail = self.details[0]
        result = convert_annotation_deitail_data(detail["data"])
        print(result)
        assert type(result) == SegmentAnnotationDetailData
        print(result.dump())
        assert result.dump() == detail["data"]

    def test_convert_annotation_deitail_data_with_cuboid(self):
        detail = self.details[1]
        result = convert_annotation_deitail_data(detail["data"])
        print(result)
        assert type(result) == CuboidAnnotationDetailData
        print(result.dump())
        print(detail["data"])
        assert result.dump() == detail["data"]

    def test_convert_annotation_deitail_data_with_other(self):
        detail = self.details[2]
        result = convert_annotation_deitail_data(detail["data"])
        print(result)
        assert type(result) == dict
