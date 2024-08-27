import ollama
from mappers.toolmap import map_function_to_ollama_tool_dict
import logging

logger = logging.getLogger(__name__)

class EasyAgent:
    def __init__(self, model, tools, system, options: ollama.Options | None = None) -> None:
        self.model = model
        self.tools = tools
        self.system = system
        self.options = options
        self.context = []

    @property
    def _tools_ollama_list(self):
        return [map_function_to_ollama_tool_dict(fn) for fn in self.tools]

    @property
    def _tools_map(self):
        return {fn.__name__: fn for fn in self.tools}

    @property
    def _system_messages(self):
        return [{'role': 'system', 'content': self.system}] if self.system is not None else []

    @property
    def _prompt_messages(self):
        """System message with memory context."""
        return self._system_messages + self.context

    def call_tool(
            self,
            name: str,
            arguments: dict[str],
            remember_response: bool = True
        ):
        logger.debug("Calling tool: %s(%s)", name, arguments)
        fn = self._tools_map[name]
        result = fn(**arguments)
        logger.debug("Tool result: %s", result)
        if remember_response:
            self.context.append({
                'role': 'tool',
                'content': result
            })
        return result

    def tick(
            self,
            prompt: str | None = None,
            remember_request: bool = True,
            remember_response: bool = True,
            ):
        """Call LLM once."""

        volatile_mem_messages = [{'role': 'user', 'content': prompt}] if prompt is not None else []
        response = ollama.chat(
            model=self.model,
            messages=self._prompt_messages + volatile_mem_messages,
            tools=self._tools_ollama_list,
            options=self.options
        )
        msg = response["message"]
        logger.debug("LLM response: %s", msg)

        if remember_request:
            self.context.extend(volatile_mem_messages)
        if remember_response:
            self.context.append(msg)

        return msg

    def ask(self, question: str) -> str:
        logger.debug("Asking: %s", question)
        response = self.tick(prompt=question)
        while True:
            if 'tool_calls' in response:
                for call in response['tool_calls']:
                    self.call_tool(**call['function'])
            else:
                break
            response = self.tick()
        
        return response['content']
