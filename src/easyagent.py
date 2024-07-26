import ollama
from mappers.toolmap import map_function_to_ollama_tool_dict

class EasyAgent:
    def __init__(self, model, tools, system) -> None:
        self.model = model
        self.tools = tools
        self.system = system
        self.context = []

    @property
    def _tools_dict(self):
        return [map_function_to_ollama_tool_dict(fn) for fn in self.tools]

    @property
    def _system_messages(self):
        return [{'role': 'system', 'content': self.system}] if self.system is not None else []

    @property
    def _messages(self):
        return self._system_messages + self.context

    def tick(
            self,
            prompt: str | None = None,
            remember_request: bool = True,
            remember_response: bool = True,
            ):
        """Call LLM once."""

        prompt_messages = [{'role': 'user', 'content': prompt}] if prompt is not None else []
        response = ollama.chat(
            model=self.model,
            messages=self._messages + prompt_messages,
            tools=self._tools_dict,
        )
        msg = response["message"]

        if remember_request:
            self.context.extend(prompt_messages)
        if remember_response:
            self.context.append(msg)

        return msg
