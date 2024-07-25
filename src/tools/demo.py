"""Function in this file is meant to check mapper."""
from typing import Optional

def demofunction(
        a: int, b: str, c: bool,
        d: int | None, e: Optional[int],
    ):
    """Some demo function description."""
    pass


def send_email(recipient: str, content: str):
    """Call this function to send an email to recipient."""
    print(f">> Sending email to <{recipient}>: \"{content}\"")
