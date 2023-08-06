from typing import TypedDict, Literal, Any, List, Dict, Union
from typing_extensions import Required


Inttoint = Dict[str, Any]
"""
IntToInt.

patternProperties:
  ^[0-9]$:
    type: integer
"""



Mappingmeta = Dict[str, Any]
"""
MappingMeta.

patternProperties:
  ^[chdfr]$:
    $ref: '#/definitions/IntToString'
"""



class Metric(TypedDict, total=False):
    """metric."""

    version: Literal[1]
    use_case_id: Required[str]
    """required"""

    org_id: Required[int]
    """required"""

    project_id: Required[int]
    """required"""

    metric_id: Required[int]
    """required"""

    type: Required[str]
    """required"""

    timestamp: Required[int]
    """required"""

    tags: Required["Inttoint"]
    """required"""

    value: Required[Union[int, List[Union[int, float]]]]
    """required"""

    retention_days: Required[int]
    """required"""

    mapping_meta: Required["Mappingmeta"]
    """required"""

