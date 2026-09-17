# from lfx.field_typing import Data
import httpx

from lfx.custom.custom_component.component import Component
from lfx.io import MessageTextInput, Output, SecretStrInput, FloatInput, IntInput
from lfx.schema.message import Message
from lfx.schema.data import Data

class CustomComponent(Component):
    display_name = "Groq Component"
    description = "Use as a template to create your own component."
    documentation: str = "https://docs.langflow.org/components-custom-components"
    icon = "groq"
    name = "GroqComponent"

    inputs = [
        MessageTextInput(name="input_value", display_name="Input Value", info="This is a custom component Input", 
            value="Hello, World!", tool_mode=True),
        SecretStrInput(name="api_key", display_name="Groq API Key", required=True,
                info="Your Groq API key (starts with gsk_). Get one at https://console.groq.com/keys"),
        MessageTextInput(name="model_name", display_name="Model", info="Groq Model Id"),
        MessageTextInput(name="system_prompt", display_name="System Prompt",
                info="Optional instruction that sets the model's behaviour.", advanced=True),
        IntInput(name="max_tokens", display_name="Max Tokens", value=1024, advanced=True),
        FloatInput(name="temperature", display_name="Temperature", value=0.7, advanced=True)
    ]

    outputs = [
        Output(display_name="Output", name="output", method="generate_response")
    ]

    def _build_messages(self) -> list[dict]:
            messages = []
            if self.system_prompt:
                messages.append({"role": "system", "content": self.system_prompt})
            messages.append({"role": "user", "content": str(self.input_value)})
            return messages

    def generate_response(self) -> Message:
            try:
                response = httpx.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": self.model_name,
                        "messages": self._build_messages(),
                        "max_tokens": self.max_tokens,
                        "temperature": self.temperature,
                    },
                    timeout=60.0,
                )
                response.raise_for_status()
            except httpx.HTTPStatusError as exc:
                raise ValueError(f"Groq API error {exc.response.status_code}: {exc.response.text}") from exc
            except httpx.HTTPError as exc:
                raise ValueError(f"Could not reach the Groq API: {exc}") from exc

            text = response.json()["choices"][0]["message"]["content"]
            self.status = text
            return Message(text=text)
