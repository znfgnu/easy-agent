from typing import Callable
from mappers.dto import OllamaTool, OllamaToolParams, OllamaToolProperty
import inspect


def map_function_to_ollama_tool_dict(fn: Callable) -> str:
    """Returns dictionary for ollama tools list."""

    return {
        "type": "function",
        "function": OllamaTool.from_function(fn).model_dump()
    }


if __name__ == "__main__":
    from tools.demo import demofunction
    d = map_function_to_ollama_tool_dict(demofunction)
    print(d)
