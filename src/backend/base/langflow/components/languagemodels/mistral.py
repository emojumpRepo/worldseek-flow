from langchain_mistralai import ChatMistralAI
from pydantic.v1 import SecretStr

from langflow.base.models.model import LCModelComponent
from langflow.field_typing import LanguageModel
from langflow.io import BoolInput, DropdownInput, FloatInput, IntInput, SecretStrInput, StrInput


class MistralAIModelComponent(LCModelComponent):
    display_name = "MistralAI"
    display_name_zh = "MistralAI"
    description = "Generates text using MistralAI LLMs."
    description_zh = "使用MistralAI大语言模型生成文本。"
    icon = "MistralAI"
    name = "MistralModel"

    inputs = [
        *LCModelComponent._base_inputs,
        IntInput(
            name="max_tokens",
            display_name="最大令牌数",
            advanced=True,
            info="The maximum number of tokens to generate. Set to 0 for unlimited tokens.",
        ),
        DropdownInput(
            name="model_name",
            display_name="模型名称",
            advanced=False,
            options=[
                "open-mixtral-8x7b",
                "open-mixtral-8x22b",
                "mistral-small-latest",
                "mistral-medium-latest",
                "mistral-large-latest",
                "codestral-latest",
            ],
            value="codestral-latest",
        ),
        StrInput(
            name="mistral_api_base",
            display_name="Mistral API Base",
            advanced=True,
            info="The base 网址 of the Mistral API. Defaults to https://api.mistral.ai/v1. "
            "You can change this to use other APIs like JinaChat, LocalAI and Prem.",
        ),
        SecretStrInput(
            name="api_key",
            display_name="Mistral API Key",
            info="The Mistral API密钥 to use for the Mistral model.",
            advanced=False,
            required=True,
            value="MISTRAL_API_KEY",
        ),
        FloatInput(
            name="temperature",
            display_name="温度",
            value=0.1,
            advanced=True,
        ),
        IntInput(
            name="max_retries",
            display_name="Max Retries",
            advanced=True,
            value=5,
        ),
        IntInput(
            name="timeout",
            display_name="超时",
            advanced=True,
            value=60,
        ),
        IntInput(
            name="max_concurrent_requests",
            display_name="Max Concurrent Requests",
            advanced=True,
            value=3,
        ),
        FloatInput(
            name="top_p",
            display_name="Top P",
            advanced=True,
            value=1,
        ),
        IntInput(
            name="random_seed",
            display_name="Random Seed",
            value=1,
            advanced=True,
        ),
        BoolInput(
            name="safe_mode",
            display_name="Safe Mode",
            advanced=True,
            value=False,
        ),
    ]

    def build_model(self) -> LanguageModel:  # type: ignore[type-var]
        try:
            return ChatMistralAI(
                model_name=self.model_name,
                mistral_api_key=SecretStr(self.api_key).get_secret_value() if self.api_key else None,
                endpoint=self.mistral_api_base or "https://api.mistral.ai/v1",
                max_tokens=self.max_tokens or None,
                temperature=self.temperature,
                max_retries=self.max_retries,
                timeout=self.timeout,
                max_concurrent_requests=self.max_concurrent_requests,
                top_p=self.top_p,
                random_seed=self.random_seed,
                safe_mode=self.safe_mode,
                streaming=self.stream,
            )
        except Exception as e:
            msg = "Could not connect to MistralAI API."
            raise ValueError(msg) from e
