from typing import Any, cast

from langflow.custom.custom_component.component import Component
from langflow.helpers.data import data_to_text
from langflow.inputs.inputs import DropdownInput, HandleInput, IntInput, MessageTextInput, MultilineInput, TabInput
from langflow.memory import aget_messages, astore_message
from langflow.schema.data import Data
from langflow.schema.dataframe import DataFrame
from langflow.schema.dotdict import dotdict
from langflow.schema.message import Message
from langflow.template.field.base import Output
from langflow.utils.component_utils import set_current_fields, set_field_display
from langflow.utils.constants import MESSAGE_SENDER_AI, MESSAGE_SENDER_NAME_AI, MESSAGE_SENDER_USER


class MemoryComponent(Component):
    display_name = "Message History"
    display_name_zh = "消息历史"
    description = "Stores or retrieves stored chat messages from Langflow tables or an external memory."
    description_zh = "从Langflow表或外部存储中存储或检索聊天消息。"
    icon = "message-square-more"
    name = "Memory"
    default_keys = ["mode", "memory"]
    mode_config = {
        "Store": ["message", "memory", "sender", "sender_name", "session_id"],
        "Retrieve": ["n_messages", "order", "template", "memory"],
    }

    inputs = [
        TabInput(
            name="mode",
            display_name="模式",
            options=["Retrieve", "Store"],
            value="Retrieve",
            info="操作模式：存储消息或检索消息。",
            real_time_refresh=True,
        ),
        MessageTextInput(
            name="message",
            display_name="消息",
            info="要存储的聊天消息。",
            tool_mode=True,
            dynamic=True,
            show=False,
        ),
        HandleInput(
            name="memory",
            display_name="外部记忆",
            input_types=["Memory"],
            info="从外部记忆中检索消息。如果为空，它将使用Langflow表。",
            advanced=True,
        ),
        DropdownInput(
            name="sender_type",
            display_name="发送者类型",
            options=[MESSAGE_SENDER_AI, MESSAGE_SENDER_USER, "Machine and User"],
            value="Machine and User",
            info="按发送者类型过滤。",
            advanced=True,
        ),
        MessageTextInput(
            name="sender",
            display_name="发送者",
            info="消息的发送者。可能是机器或用户。如果为空，将使用当前发送者参数。",
            advanced=True,
        ),
        MessageTextInput(
            name="sender_name",
            display_name="发送者名称",
            info="按发送者名称过滤。",
            advanced=True,
            show=False,
        ),
        IntInput(
            name="n_messages",
            display_name="消息数量",
            value=100,
            info="要检索的消息数量。",
            advanced=True,
            show=True,
        ),
        MessageTextInput(
            name="session_id",
            display_name="会话ID",
            info="聊天会话ID。如果为空，将使用当前会话ID参数。",
            value="",
            advanced=True,
        ),
        DropdownInput(
            name="order",
            display_name="顺序",
            options=["Ascending", "Descending"],
            value="Ascending",
            info="消息的顺序。",
            advanced=True,
            tool_mode=True,
            required=True,
        ),
        MultilineInput(
            name="template",
            display_name="模板",
            info="用于格式化数据的模板。"
            "它可以包含{text}、{sender}或其他消息数据中的任何其他键。",
            value="{sender_name}: {text}",
            advanced=True,
            show=False,
        ),
    ]

    outputs = [
        Output(display_name="消息", name="messages_text", method="retrieve_messages_as_text", dynamic=True),
        Output(display_name="Dataframe", name="dataframe", method="retrieve_messages_dataframe", dynamic=True),
    ]

    def update_outputs(self, frontend_node: dict, field_name: str, field_value: Any) -> dict:
        """Dynamically show only the relevant output based on the selected output type."""
        if field_name == "mode":
            # Start with empty outputs
            frontend_node["outputs"] = []
            if field_value == "Store":
                frontend_node["outputs"] = [
                    Output(
                        display_name="Stored Messages",
                        name="stored_messages",
                        method="store_message",
                        hidden=True,
                        dynamic=True,
                    )
                ]
            if field_value == "Retrieve":
                frontend_node["outputs"] = [
                    Output(
                        display_name="Messages", name="messages_text", method="retrieve_messages_as_text", dynamic=True
                    ),
                    Output(
                        display_name="Dataframe", name="dataframe", method="retrieve_messages_dataframe", dynamic=True
                    ),
                ]
        return frontend_node

    async def store_message(self) -> Message:
        message = Message(text=self.message) if isinstance(self.message, str) else self.message

        message.session_id = self.session_id or message.session_id
        message.sender = self.sender or message.sender or MESSAGE_SENDER_AI
        message.sender_name = self.sender_name or message.sender_name or MESSAGE_SENDER_NAME_AI

        stored_messages: list[Message] = []

        if self.memory:
            self.memory.session_id = message.session_id
            lc_message = message.to_lc_message()
            await self.memory.aadd_messages([lc_message])

            stored_messages = await self.memory.aget_messages() or []

            stored_messages = [Message.from_lc_message(m) for m in stored_messages] if stored_messages else []

            if message.sender:
                stored_messages = [m for m in stored_messages if m.sender == message.sender]
        else:
            await astore_message(message, flow_id=self.graph.flow_id)
            stored_messages = (
                await aget_messages(
                    session_id=message.session_id, sender_name=message.sender_name, sender=message.sender
                )
                or []
            )

        if not stored_messages:
            msg = "No messages were stored. Please ensure that the session ID and sender are properly set."
            raise ValueError(msg)

        stored_message = stored_messages[0]
        self.status = stored_message
        return stored_message

    async def retrieve_messages(self) -> Data:
        sender_type = self.sender_type
        sender_name = self.sender_name
        session_id = self.session_id
        n_messages = self.n_messages
        order = "DESC" if self.order == "Descending" else "ASC"

        if sender_type == "Machine and User":
            sender_type = None

        if self.memory and not hasattr(self.memory, "aget_messages"):
            memory_name = type(self.memory).__name__
            err_msg = f"External Memory object ({memory_name}) must have 'aget_messages' method."
            raise AttributeError(err_msg)
        # Check if n_messages is None or 0
        if n_messages == 0:
            stored = []
        elif self.memory:
            # override session_id
            self.memory.session_id = session_id

            stored = await self.memory.aget_messages()
            # langchain memories are supposed to return messages in ascending order

            if order == "DESC":
                stored = stored[::-1]
            if n_messages:
                stored = stored[-n_messages:] if order == "ASC" else stored[:n_messages]
            stored = [Message.from_lc_message(m) for m in stored]
            if sender_type:
                expected_type = MESSAGE_SENDER_AI if sender_type == MESSAGE_SENDER_AI else MESSAGE_SENDER_USER
                stored = [m for m in stored if m.type == expected_type]
        else:
            # For internal memory, we always fetch the last N messages by ordering by DESC
            stored = await aget_messages(
                sender=sender_type,
                sender_name=sender_name,
                session_id=session_id,
                limit=10000,
                order=order,
            )
            if n_messages:
                stored = stored[-n_messages:] if order == "ASC" else stored[:n_messages]

        # self.status = stored
        return cast(Data, stored)

    async def retrieve_messages_as_text(self) -> Message:
        stored_text = data_to_text(self.template, await self.retrieve_messages())
        # self.status = stored_text
        return Message(text=stored_text)

    async def retrieve_messages_dataframe(self) -> DataFrame:
        """Convert the retrieved messages into a DataFrame.

        Returns:
            DataFrame: A DataFrame containing the message data.
        """
        messages = await self.retrieve_messages()
        return DataFrame(messages)

    def update_build_config(
        self,
        build_config: dotdict,
        field_value: Any,  # noqa: ARG002
        field_name: str | None = None,  # noqa: ARG002
    ) -> dotdict:
        return set_current_fields(
            build_config=build_config,
            action_fields=self.mode_config,
            selected_action=build_config["mode"]["value"],
            default_fields=self.default_keys,
            func=set_field_display,
        )
