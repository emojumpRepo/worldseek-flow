from collections.abc import Generator
from typing import Any

import orjson
from fastapi.encoders import jsonable_encoder

from langflow.base.io.chat import ChatComponent
from langflow.helpers.data import safe_convert
from langflow.inputs.inputs import BoolInput, DropdownInput, HandleInput, MessageTextInput
from langflow.schema.data import Data
from langflow.schema.dataframe import DataFrame
from langflow.schema.message import Message
from langflow.schema.properties import Source
from langflow.template.field.base import Output
from langflow.utils.constants import (
    MESSAGE_SENDER_AI,
    MESSAGE_SENDER_NAME_AI,
    MESSAGE_SENDER_USER,
)


class ChatOutput(ChatComponent):
    display_name = "Chat Output"
    display_name_zh = "聊天输出"
    description = "Display a chat message in the Playground."
    description_zh = "在游乐场中显示聊天消息。"
    icon = "MessagesSquare"
    name = "ChatOutput"
    minimized = True

    inputs = [
        HandleInput(
            name="input_value",
            display_name="输入",
            info="要作为输出传递的消息。",
            input_types=["Data", "DataFrame", "Message"],
            required=True,
        ),
        BoolInput(
            name="should_store_message",
            display_name="存储消息",
            info="将消息存储在历史记录中。",
            value=True,
            advanced=True,
        ),
        DropdownInput(
            name="sender",
            display_name="发送者类型",
            options=[MESSAGE_SENDER_AI, MESSAGE_SENDER_USER],
            value=MESSAGE_SENDER_AI,
            advanced=True,
            info="发送者类型。",
        ),
        MessageTextInput(
            name="sender_name",
            display_name="发送者名称",
            info="发送者名称。",
            value=MESSAGE_SENDER_NAME_AI,
            advanced=True,
        ),
        MessageTextInput(
            name="session_id",
            display_name="会话ID",
            info="聊天的会话ID。如果为空，将使用当前会话ID参数。",
            advanced=True,
        ),
        MessageTextInput(
            name="data_template",
            display_name="数据模板",
            value="{text}",
            advanced=True,
            info="将数据转换为文本的模板。如果留空，将动态设置为数据的文本键。",
        ),
        MessageTextInput(
            name="background_color",
            display_name="背景颜色",
            info="图标的背景颜色。",
            advanced=True,
        ),
        MessageTextInput(
            name="chat_icon",
            display_name="图标",
            info="消息的图标。",
            advanced=True,
        ),
        MessageTextInput(
            name="text_color",
            display_name="文本颜色",
            info="名称的文本颜色。",
            advanced=True,
        ),
        BoolInput(
            name="clean_data",
            display_name="基础数据清理",
            value=True,
            info="是否清理数据。",
            advanced=True,
        ),
    ]
    outputs = [
        Output(
            display_name="输出消息",
            name="message",
            method="message_response",
        ),
    ]

    def _build_source(self, id_: str | None, display_name: str | None, source: str | None) -> Source:
        source_dict = {}
        if id_:
            source_dict["id"] = id_
        if display_name:
            source_dict["display_name"] = display_name
        if source:
            # Handle case where source is a ChatOpenAI object
            if hasattr(source, "model_name"):
                source_dict["source"] = source.model_name
            elif hasattr(source, "model"):
                source_dict["source"] = str(source.model)
            else:
                source_dict["source"] = str(source)
        return Source(**source_dict)

    async def message_response(self) -> Message:
        # First convert the input to string if needed
        text = self.convert_to_string()

        # Get source properties
        source, icon, display_name, source_id = self.get_properties_from_source_component()
        background_color = self.background_color
        text_color = self.text_color
        if self.chat_icon:
            icon = self.chat_icon

        # Create or use existing Message object
        if isinstance(self.input_value, Message):
            message = self.input_value
            # Update message properties
            message.text = text
        else:
            message = Message(text=text)

        # Set message properties
        message.sender = self.sender
        message.sender_name = self.sender_name
        message.session_id = self.session_id
        message.flow_id = self.graph.flow_id if hasattr(self, "graph") else None
        message.properties.source = self._build_source(source_id, display_name, source)
        message.properties.icon = icon
        message.properties.background_color = background_color
        message.properties.text_color = text_color

        # Store message if needed
        if self.session_id and self.should_store_message:
            stored_message = await self.send_message(message)
            self.message.value = stored_message
            message = stored_message

        self.status = message
        return message

    def _serialize_data(self, data: Data) -> str:
        """Serialize Data object to JSON string."""
        # Convert data.data to JSON-serializable format
        serializable_data = jsonable_encoder(data.data)
        # Serialize with orjson, enabling pretty printing with indentation
        json_bytes = orjson.dumps(serializable_data, option=orjson.OPT_INDENT_2)
        # Convert bytes to string and wrap in Markdown code blocks
        return "```json\n" + json_bytes.decode("utf-8") + "\n```"

    def _validate_input(self) -> None:
        """Validate the input data and raise ValueError if invalid."""
        if self.input_value is None:
            msg = "Input data cannot be None"
            raise ValueError(msg)
        if isinstance(self.input_value, list) and not all(
            isinstance(item, Message | Data | DataFrame | str) for item in self.input_value
        ):
            invalid_types = [
                type(item).__name__
                for item in self.input_value
                if not isinstance(item, Message | Data | DataFrame | str)
            ]
            msg = f"Expected Data or DataFrame or Message or str, got {invalid_types}"
            raise TypeError(msg)
        if not isinstance(
            self.input_value,
            Message | Data | DataFrame | str | list | Generator | type(None),
        ):
            type_name = type(self.input_value).__name__
            msg = f"Expected Data or DataFrame or Message or str, Generator or None, got {type_name}"
            raise TypeError(msg)

    def convert_to_string(self) -> str | Generator[Any, None, None]:
        """Convert input data to string with proper error handling."""
        self._validate_input()
        if isinstance(self.input_value, list):
            return "\n".join([safe_convert(item, clean_data=self.clean_data) for item in self.input_value])
        if isinstance(self.input_value, Generator):
            return self.input_value
        return safe_convert(self.input_value)
