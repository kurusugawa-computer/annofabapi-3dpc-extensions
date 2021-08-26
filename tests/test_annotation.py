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


def test_convert_annotation_deitail_data():
    with (data_dir / "simple_annotation.json").open() as f:
        dict_simple_annotation = json.load(f)

    details = dict_simple_annotation["details"]

    result0 = convert_annotation_deitail_data(details[0]["data"])
    print(result0)
    assert type(result0) == SegmentAnnotationDetailData

    result1 = convert_annotation_deitail_data(details[1]["data"])
    print(result1)
    assert type(result1) == CuboidAnnotationDetailData
