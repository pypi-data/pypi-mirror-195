from typing import Union, TypedDict, Literal, Any, Dict, List
from typing_extensions import Required


class GenericMetric(TypedDict, total=False):
    """generic_metric."""

    version: Literal[2]
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

    tags: Required["Inttostring"]
    """required"""

    value: Required[Union[int, List[Union[int, float]]]]
    """required"""

    retention_days: Required[int]
    """required"""

    mapping_meta: Required["Mappingmeta"]
    """required"""



Inttostring = Dict[str, Any]
"""
IntToString.

patternProperties:
  ^.*$:
    type: string
"""



Mappingmeta = Dict[str, Any]
"""
MappingMeta.

patternProperties:
  ^[chdfr]$:
    $ref: '#/definitions/IntToString'
"""

