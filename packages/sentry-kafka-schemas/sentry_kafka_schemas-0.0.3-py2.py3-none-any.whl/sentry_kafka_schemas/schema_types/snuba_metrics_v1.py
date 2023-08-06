from typing import Dict, List, Literal, TypedDict, Any, Union


Inttoint = Dict[str, Any]
"""
IntToInt.

patternProperties:
  ^[0-9]$:
    type: integer
"""



class Main(TypedDict, total=False):
    """Main."""

    version: Literal[1]
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

    tags: "Inttoint"
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

