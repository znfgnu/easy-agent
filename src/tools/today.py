import datetime

def now() -> str:
    """Call this function when you want to get current date and time."""
    return datetime.datetime.now().isoformat()
