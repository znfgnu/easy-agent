import datetime
from args_description import describe_args

@describe_args()
def now() -> str:
    """Call this function when you want to get current date and time."""
    return datetime.datetime.now().isoformat()[:-7]
