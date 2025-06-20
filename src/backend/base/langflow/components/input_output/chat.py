from langflow.base.data.utils import IMG_FILE_TYPES, TEXT_FILE_TYPES
from langflow.base.io.chat import ChatComponent
from langflow.inputs.inputs import BoolInput
from langflow.io import (
    DropdownInput,
    FileInput,
    MessageTextInput,
    MultilineInput,
    Output,
)
from langflow.schema.message import Message
from langflow.utils.constants import (
    MESSAGE_SENDER_AI,
    MESSAGE_SENDER_NAME_USER,
    MESSAGE_SENDER_USER,
)


class ChatInput(ChatComponent):
    display_name = "Chat Input"
    display_name_zh = "聊天输入"
    description = "Get chat inputs from the Playground."
    description_zh = "获取用户的聊天输入。"
    icon = "MessagesSquare"
    name = "ChatInput"
    minimized = True

    inputs = [
        MultilineInput(
            name="input_value",
            display_name="输入文本",
            value="",
            info="要作为输入传递的消息。",
            input_types=[],
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
            value=MESSAGE_SENDER_USER,
            info="发送者类型。",
            advanced=True,
        ),
        MessageTextInput(
            name="sender_name",
            display_name="发送者名称",
            info="发送者名称。",
            value=MESSAGE_SENDER_NAME_USER,
            advanced=True,
        ),
        MessageTextInput(
            name="session_id",
            display_name="会话ID",
            info="聊天会话ID。如果为空，则使用当前会话ID参数。",
            advanced=True,
        ),
        FileInput(
            name="files",
            display_name="文件",
            file_types=TEXT_FILE_TYPES + IMG_FILE_TYPES,
            info="要与消息一起发送的文件。",
            advanced=True,
            is_list=True,
            temp_file=True,
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
    ]
    outputs = [
        Output(display_name="聊天消息", name="message", method="message_response"),
    ]

    async def message_response(self) -> Message:
        background_color = self.background_color
        text_color = self.text_color
        icon = self.chat_icon

        message = await Message.create(
            text=self.input_value,
            sender=self.sender,
            sender_name=self.sender_name,
            session_id=self.session_id,
            files=self.files,
            properties={
                "background_color": background_color,
                "text_color": text_color,
                "icon": icon,
            },
        )
        if self.session_id and isinstance(message, Message) and self.should_store_message:
            stored_message = await self.send_message(
                message,
            )
            self.message.value = stored_message
            message = stored_message

        self.status = message
        return message
