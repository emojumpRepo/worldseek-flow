from loguru import logger

from langflow.custom.custom_component.component import Component
from langflow.io import MessageInput, Output
from langflow.schema.data import Data
from langflow.schema.message import Message


class MessageToDataComponent(Component):
    display_name = "Message to Data"
    display_name_zh = "消息 → 数据"
    description = "Convert a Message object to a Data object"
    description_zh = "将消息对象转换为数据对象"
    icon = "message-square-share"
    beta = True
    name = "MessagetoData"
    legacy = True

    inputs = [
        MessageInput(
            name="message",
            display_name="消息",
            info="要转换为数据对象的消息对象",
        ),
    ]

    outputs = [
        Output(display_name="数据", name="data", method="convert_message_to_data"),
    ]

    def convert_message_to_data(self) -> Data:
        if isinstance(self.message, Message):
            # Convert Message to Data
            return Data(data=self.message.data)

        msg = "Error converting Message to Data: Input must be a Message object"
        logger.opt(exception=True).debug(msg)
        self.status = msg
        return Data(data={"error": msg})
