# annofabapi-3dpc-extensions
[annofabapi](https://github.com/kurusugawa-computer/annofab-api-python-client)の3DPC（3D Point Cloud） Editor用の拡張機能です。

# Install

```
$ pip install annofabapi-3dpc-extensions
```


# Usage

cuboidアノテーションやセグメントアノテーションに対応した

```python
from annofabapi.parser import SimpleAnnotationDirParser

from annofab_3dpc.annotation import (
    CuboidAnnotationDecodeError,
    CuboidAnnotationDetailDataV1,
    CuboidAnnotationDetailDataV2,
    EulerAnglesZXY,
    Location,
    SegmentAnnotationDetailData,
    convert_annotation_detail_data,
)

parser = SimpleAnnotationDirParser("annotation/task1/input1.json")
result = parser.parse(convert_annotation_detail_data)
assert type(result.details[0].data) == SegmentAnnotationDetailData
assert type(result.details[1].data) == CuboidAnnotationDetailDataV2
assert type(result.details[2].data) == CuboidAnnotationDetailDataV1
assert type(result.details[3].data) == dict

```
