from typing import Any

from langchain_openai import OpenAIEmbeddings

from langflow.base.embeddings.model import LCEmbeddingsModel
from langflow.base.models.openai_constants import OPENAI_EMBEDDING_MODEL_NAMES
from langflow.field_typing import Embeddings
from langflow.io import (
    BoolInput,
    DictInput,
    DropdownInput,
    FloatInput,
    IntInput,
    MessageTextInput,
    SecretStrInput,
)
from langflow.schema.dotdict import dotdict


class EmbeddingModelComponent(LCEmbeddingsModel):
    display_name = "Embedding Model"
    display_name_zh = "Embedding模型"
    description = "Generate embeddings using a specified provider."
    description_zh = "使用指定的模型提供商生成嵌入。"
    icon = "binary"
    name = "EmbeddingModel"
    category = "models"

    inputs = [
        DropdownInput(
            name="provider",
            display_name="模型提供商",
            options=["OpenAI"],
            value="OpenAI",
            info="选择嵌入模型提供商",
            real_time_refresh=True,
            options_metadata=[{"icon": "OpenAI"}],
        ),
        DropdownInput(
            name="model",
            display_name="模型名称",
            options=OPENAI_EMBEDDING_MODEL_NAMES,
            value=OPENAI_EMBEDDING_MODEL_NAMES[0],
            info="选择要使用的嵌入模型",
        ),
        SecretStrInput(
            name="api_key",
            display_name="API Key",
            info="模型提供商的API Key",
            required=True,
            show=True,
            real_time_refresh=True,
        ),
        MessageTextInput(
            name="api_base",
            display_name="API Base URL",
            info="API的Base网址。留空使用默认值。",
            advanced=True,
        ),
        IntInput(
            name="dimensions",
            display_name="维度",
            info="输出嵌入的维度。仅支持某些模型。",
            advanced=True,
        ),
        IntInput(name="chunk_size", display_name="块大小", advanced=True, value=1000),
        FloatInput(name="request_timeout", display_name="请求超时", advanced=True),
        IntInput(name="max_retries", display_name="最大重试次数", advanced=True, value=3),
        BoolInput(name="show_progress_bar", display_name="显示进度条", advanced=True),
        DictInput(
            name="model_kwargs",
            display_name="模型参数",
            advanced=True,
            info="要传递给模型的附加关键字参数。",
        ),
    ]

    def build_embeddings(self) -> Embeddings:
        provider = self.provider
        model = self.model
        api_key = self.api_key
        api_base = self.api_base
        dimensions = self.dimensions
        chunk_size = self.chunk_size
        request_timeout = self.request_timeout
        max_retries = self.max_retries
        show_progress_bar = self.show_progress_bar
        model_kwargs = self.model_kwargs or {}

        if provider == "OpenAI":
            if not api_key:
                msg = "OpenAI API Key 是使用OpenAI提供商时必需的"
                raise ValueError(msg)
            return OpenAIEmbeddings(
                model=model,
                dimensions=dimensions or None,
                base_url=api_base or None,
                api_key=api_key,
                chunk_size=chunk_size,
                max_retries=max_retries,
                timeout=request_timeout or None,
                show_progress_bar=show_progress_bar,
                model_kwargs=model_kwargs,
            )
        msg = f"Unknown provider: {provider}"
        raise ValueError(msg)

    def update_build_config(self, build_config: dotdict, field_value: Any, field_name: str | None = None) -> dotdict:
        if field_name == "provider" and field_value == "OpenAI":
            build_config["model"]["options"] = OPENAI_EMBEDDING_MODEL_NAMES
            build_config["model"]["value"] = OPENAI_EMBEDDING_MODEL_NAMES[0]
            build_config["api_key"]["display_name"] = "OpenAI API Key"
            build_config["api_base"]["display_name"] = "OpenAI API Base URL"
        return build_config
