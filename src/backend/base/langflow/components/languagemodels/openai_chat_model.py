from typing import Any

from langchain_openai import ChatOpenAI
from pydantic.v1 import SecretStr

from langflow.base.models.model import LCModelComponent
from langflow.base.models.openai_constants import (
    OPENAI_MODEL_NAMES,
    OPENAI_REASONING_MODEL_NAMES,
)
from langflow.field_typing import LanguageModel
from langflow.field_typing.range_spec import RangeSpec
from langflow.inputs.inputs import BoolInput, DictInput, DropdownInput, IntInput, SecretStrInput, SliderInput, StrInput
from langflow.logging import logger


class OpenAIModelComponent(LCModelComponent):
    display_name = "OpenAI"
    display_name_zh = "OpenAI"
    description = "Generates text using OpenAI LLMs."
    description_zh = "使用OpenAI大语言模型生成文本。"
    icon = "OpenAI"
    name = "OpenAIModel"

    inputs = [
        *LCModelComponent._base_inputs,
        IntInput(
            name="max_tokens",
            display_name="最大令牌数",
            advanced=True,
            info="要生成的最大令牌数。设置为0表示无限制。",
            range_spec=RangeSpec(min=0, max=128000),
        ),
        DictInput(
            name="model_kwargs",
            display_name="模型参数",
            advanced=True,
            info="要传递给模型的附加关键字参数。",
        ),
        BoolInput(
            name="json_mode",
            display_name="JSON模式",
            advanced=True,
            info="如果为真，将输出JSON，无论是否传递模式。",
        ),
        DropdownInput(
            name="model_name",
            display_name="模型名称",
            advanced=False,
            options=OPENAI_MODEL_NAMES + OPENAI_REASONING_MODEL_NAMES,
            value=OPENAI_MODEL_NAMES[1],
            combobox=True,
            real_time_refresh=True,
        ),
        StrInput(
            name="openai_api_base",
            display_name="OpenAI API基础URL",
            advanced=True,
            info="OpenAI API的基础URL。默认为https://api.openai.com/v1. "
            "您可以更改此URL以使用其他API，如JinaChat、LocalAI和Prem。",
        ),
        SecretStrInput(
            name="api_key",
            display_name="OpenAI API密钥",
            info="用于OpenAI模型的OpenAI API密钥。",
            advanced=False,
            value="OPENAI_API_KEY",
            required=True,
        ),
        SliderInput(
            name="temperature",
            display_name="温度",
            value=0.1,
            range_spec=RangeSpec(min=0, max=1, step=0.01),
            show=True,
        ),
        IntInput(
            name="seed",
            display_name="随机种子",
            info="随机种子控制任务的可重复性。",
            advanced=True,
            value=1,
        ),
        IntInput(
            name="max_retries",
            display_name="最大重试次数",
            info="生成时最大重试次数。",
            advanced=True,
            value=5,
        ),
        IntInput(
            name="timeout",
            display_name="超时",
            info="OpenAI完成API请求的超时时间。",
            advanced=True,
            value=700,
        ),
    ]

    def build_model(self) -> LanguageModel:  # type: ignore[type-var]
        parameters = {
            "api_key": SecretStr(self.api_key).get_secret_value() if self.api_key else None,
            "model_name": self.model_name,
            "max_tokens": self.max_tokens or None,
            "model_kwargs": self.model_kwargs or {},
            "base_url": self.openai_api_base or "https://api.openai.com/v1",
            "seed": self.seed,
            "max_retries": self.max_retries,
            "timeout": self.timeout,
            "temperature": self.temperature if self.temperature is not None else 0.1,
        }

        logger.info(f"Model name: {self.model_name}")
        if self.model_name in OPENAI_REASONING_MODEL_NAMES:
            logger.info("Getting reasoning model parameters")
            parameters.pop("temperature")
            parameters.pop("seed")
        output = ChatOpenAI(**parameters)
        if self.json_mode:
            output = output.bind(response_format={"type": "json_object"})

        return output

    def _get_exception_message(self, e: Exception):
        """Get a message from an OpenAI exception.

        Args:
            e (Exception): The exception to get the message from.

        Returns:
            str: The message from the exception.
        """
        try:
            from openai import BadRequestError
        except ImportError:
            return None
        if isinstance(e, BadRequestError):
            message = e.body.get("message")
            if message:
                return message
        return None

    def update_build_config(self, build_config: dict, field_value: Any, field_name: str | None = None) -> dict:
        if field_name in {"base_url", "model_name", "api_key"} and field_value in OPENAI_REASONING_MODEL_NAMES:
            build_config["temperature"]["show"] = False
            build_config["seed"]["show"] = False
        if field_name in {"base_url", "model_name", "api_key"} and field_value in OPENAI_MODEL_NAMES:
            build_config["temperature"]["show"] = True
            build_config["seed"]["show"] = True
        return build_config
