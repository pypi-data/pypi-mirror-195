from typing import List, TypedDict, Literal, Any, Dict, Union


Inttostring = Dict[str, Any]
"""
IntToString.

patternProperties:
  ^.*$:
    type: string
"""



class Main(TypedDict, total=False):
    """Main."""

    version: Literal[2]
    use_case_id: str
    """required"""

    org_id: int
    """required"""

    project_id: int
    """required"""

    metric_id: int
    """required"""

    type: str
    """required"""

    timestamp: int
    """required"""

    tags: "Inttostring"
    """required"""

    value: Union[int, List[Union[int, float]]]
    """required"""

    retention_days: int
    """required"""

    mapping_meta: "Mappingmeta"
    """required"""



Mappingmeta = Dict[str, Any]
"""
MappingMeta.

patternProperties:
  ^[chdfr]$:
    $ref: '#/definitions/IntToString'
"""

