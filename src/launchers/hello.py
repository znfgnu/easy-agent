from easyagent import EasyAgent
from tools.today import now
from pprint import pprint

ea = EasyAgent(
    model="llama3.1:8b",
    tools=[now],
    system=None,
)

response = ea.ask("What is the date today?")
pprint(response)
