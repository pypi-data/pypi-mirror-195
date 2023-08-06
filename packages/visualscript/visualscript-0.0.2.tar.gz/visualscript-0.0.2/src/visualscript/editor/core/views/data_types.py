from types import UnionType
from typing import Any
from PyQt5.QtGui import QColor
from editor.core.models.data_types import EXEC, WILDCARD, HANDLE

TYPE_COLORS = {
    EXEC: QColor("#FFFFFFFF"),
    HANDLE: QColor("#FFCC1111"),
    Any: QColor("#FF666666"),
    type: QColor("#FF880088"),
    bool: QColor("#FF880000"),
    float: QColor("#FF6CB149"),
    int: QColor("#FF52e220"),
    str: QColor("#FFF222b0"),
    # Union: QColor("#FF00FFFF"),
    UnionType: QColor("#FF00FFFF"),
}
OBJECT_COLOR = QColor("#FF22b0F2")
UNION_COLOR = QColor("#FFFF9900")