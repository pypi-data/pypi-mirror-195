from typing import List, TypedDict, Dict, Union, Any


class Querylog(TypedDict, total=False):
    """
    Querylog.

    Querylog schema
    """

    request: "_QuerylogRequest"
    """
    WARNING: The required are not correctly taken in account,
    See: https://github.com/camptocamp/jsonschema-gentypes/issues/6

    required
    """

    dataset: str
    """required"""

    entity: str
    """required"""

    start_timestamp: Union[int, None]
    """required"""

    end_timestamp: Union[int, None]
    """required"""

    status: str
    """required"""

    projects: List[int]
    """required"""

    query_list: List["_QuerylogQueryListItem"]
    """required"""

    timing: "_QuerylogTiming"
    """
    WARNING: The required are not correctly taken in account,
    See: https://github.com/camptocamp/jsonschema-gentypes/issues/6

    required
    """

    snql_anonymized: str


class _QuerylogQueryListItem(TypedDict, total=False):
    sql: str
    """required"""

    sql_anonymized: str
    """required"""

    start_timestamp: Union[int, None]
    """required"""

    end_timestamp: Union[int, None]
    """required"""

    stats: Dict[str, Any]
    """required"""

    status: str
    """required"""

    trace_id: Union[str, None]
    """required"""

    profile: Dict[str, Any]
    """required"""

    result_profile: Union[Dict[str, Any], None]
    """required"""



class _QuerylogRequest(TypedDict, total=False):
    id: str
    body: Dict[str, Any]
    referrer: str


class _QuerylogTiming(TypedDict, total=False):
    timestamp: int
    duration_ms: int
    marks_ms: Dict[str, Any]
    tags: Dict[str, Any]
