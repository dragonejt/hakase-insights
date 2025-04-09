from datetime import datetime, timezone

from langchain_core.tools import tool


@tool
def current_time() -> str:
    """
    Gets the current time in UTC timezone
    Parameters: None
    Returns: str: Current time in ISO 8601 format
    """
    return datetime.now(timezone.utc).isoformat()
