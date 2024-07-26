from easyagent import EasyAgent
from tools.today import now
from pprint import pprint

ea = EasyAgent(
    model="llama3.1:8b",
    tools=[now],
    system=None,
)
pprint(ea.tick("What is the date today?"))
