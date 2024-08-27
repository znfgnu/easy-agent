from easyagent import EasyAgent
from tools.today import now
from pprint import pprint
from args_description import describe_args
from agents.calendar_agent import CalendarAgent

import logging


logger = logging.getLogger(__name__)


ca = CalendarAgent(
    email="your-email@gmail.com",
    model="llama3.1:8b",
)


@describe_args(
    request="Natural language request to the calendar app.",
)
def calendar(request: str):
    """Call this function to perform calendar-related action."""
    logger.debug("Calendar request: %s", request)
    # print(f">> Sending email to <{recipient}>: \"{content}\"")
    # return "11:30PM: Baking donuts"
    return ca.ask(request)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    )
    logging.getLogger('httpcore').setLevel(logging.INFO)
    logging.getLogger('httpx').setLevel(logging.ERROR)
    logging.getLogger('googleapiclient.discovery').setLevel(logging.ERROR)

    ea = EasyAgent(
        model="llama3.1:8b",
        tools=[now, calendar],
        system="You are my personal assistant.",
    )

    # Needs to be asked to determine when "tomorrow" is
    ca.ask("What's the date today?")
    
    # response = ea.ask("What is the date today?")
    # pprint(response)
    response = ea.ask("What meetings do I have tomorrow?")
    pprint(response)
    # pprint(f"{i}: {response}")
