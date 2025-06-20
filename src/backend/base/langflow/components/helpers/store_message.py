from langflow.custom.custom_component.component import Component
from langflow.inputs.inputs import (
    HandleInput,
    MessageTextInput,
)
from langflow.memory import aget_messages, astore_message
from langflow.schema.message import Message
from langflow.template.field.base import Output
from langflow.utils.constants import MESSAGE_SENDER_AI, MESSAGE_SENDER_NAME_AI


class MessageStoreComponent(Component):
    display_name = "Message Store"
    display_name_zh = "消息存储"
    description = "Stores a chat message or text into Langflow tables or an external memory."
    description_zh = "将聊天消息或文本存储到Langflow表或外部内存中。"
    icon = "message-square-text"
    name = "StoreMessage"
    legacy = True

    inputs = [
        MessageTextInput(
            name="message", display_name="消息", info="要存储的聊天消息。", required=True, tool_mode=True
        ),
        HandleInput(
            name="memory",
            display_name="外部内存",
            input_types=["Memory"],
            info="要存储消息的外部内存。如果为空，将使用Langflow表。",
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
            info="消息发送者的名称。可能是AI或用户。如果为空，将使用当前发送者参数。",
            advanced=True,
        ),
        MessageTextInput(
            name="session_id",
            display_name="会话ID",
            info="聊天会话ID。如果为空，将使用当前会话ID参数。",
            value="",
            advanced=True,
        ),
    ]

    outputs = [
        Output(display_name="存储的消息", name="stored_messages", method="store_message", hidden=True),
    ]

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
