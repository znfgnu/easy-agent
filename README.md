EasyAgent
===

Ollama tool calling agent framework.

Using this framework you can run a single agent with lightweight tools framework.

[Ollama: Tool support (blogpost)](https://ollama.com/blog/tool-support)

# Usage
```python
import datetime
from args_description import describe_args

@describe_args()
def now() -> str:
    """Call this function when you want to get current date and time."""
    return datetime.datetime.now().isoformat()

ea = EasyAgent(
    model="llama3.1:8b",
    tools=[now],
    system=None,
)

ea.ask("What is the date today?")
# 'The current date is July 26, 2024.'

ea.tick("What is the date today?")
# {'content': '',
#  'role': 'assistant',
#  'tool_calls': [{'function': {'arguments': {}, 'name': 'now'}}]}

```

# Installation

```shell
python3 -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt
python3 ./src/launchers/hello.py
```
