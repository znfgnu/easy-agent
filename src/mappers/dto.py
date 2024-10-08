from collections import defaultdict
from inspect import Parameter, Signature, signature
from pydantic import BaseModel
import warnings


class OllamaToolProperty(BaseModel):
    type: str
    description: str | None
    enum: list[str] | None = None

    @classmethod
    def from_param(cls, param: Parameter, description: str):
        available_annotations = {
            int: "number",
            str: "string",
            bool: "boolean",
        }

        type_name = "object"
        required = []
        for type_, name in available_annotations.items():
            # Create sample instance
            sample = type_()
            # Check if compatible with annotation
            if isinstance(sample, param.annotation):
                # Select name
                type_name = name
                break

        return cls(
            type=type_name,
            description=description,
        )


class OllamaToolParams(BaseModel):
    type: str
    required: list[str]
    properties: dict[str, OllamaToolProperty]

    @classmethod
    def from_callable(cls, fn: callable):
        sig = signature(fn)
        params = sig.parameters.copy()
        if hasattr(fn, "__descriptions__"):
            descriptions = fn.__descriptions__
        else:
            import textwrap
            warnings.warn(textwrap.dedent(f"""
                Descriptions for "{fn.__name__}" tool's arguments are not defined.
                Will become empty strings in prompt."""))
            descriptions = dict()
        return cls(
            type="object",
            properties={
                name: OllamaToolProperty.from_param(
                    param=param,
                    description=descriptions.get(name, None)
                )
                for name, param in params.items()
            },
            required=[
                # Add to required if not optional <- None passes check
                name
                for name, param in params.items()
                if not isinstance(None, param.annotation)
            ]
        )


class OllamaTool(BaseModel):
    name: str
    description: str
    parameters: OllamaToolParams

    @classmethod
    def from_function(cls, fn: callable):
        return cls(
            name=fn.__name__,
            description=fn.__doc__,
            parameters=OllamaToolParams.from_callable(fn=fn)
        )
