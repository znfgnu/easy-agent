"""Function in this file is meant to check mapper."""
from typing import Optional
from args_description import describe_args

@describe_args(
        a="some integer",
        b="some string",
        c="some boolean value",
        d="optional: another number",
        e="optional: another int",
)
def demo_function(
        a: int,
        b: str,
        c: bool,
        d: int | None,
        e: Optional[int],
    ):
    """Some demo function description."""
    pass


@describe_args(
        recipient="Recipient's email address",
        # intentionally omitted content
)
def send_email(recipient: str, content: str):
    """Call this function to send an email to recipient."""
    print(f">> Sending email to <{recipient}>: \"{content}\"")
