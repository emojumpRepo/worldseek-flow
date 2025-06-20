from langflow.custom.custom_component.component import Component
from langflow.io import MessageInput
from langflow.schema.message import Message
from langflow.template.field.base import Output


class PassMessageComponent(Component):
    display_name = "Pass"
    display_name_zh = "传递消息"
    description = "Forwards the input message, unchanged."
    description_zh = "传递输入消息，不修改消息内容。"
    name = "Pass"
    icon = "arrow-right"
    legacy: bool = True

    inputs = [
        MessageInput(
            name="input_message",
            display_name="输入消息",
            info="要传递的消息。",
            required=True,
        ),
        MessageInput(
            name="ignored_message",
            display_name="忽略消息",
            info="要忽略的第二个消息。用于解决连续性问题。",
            advanced=True,
        ),
    ]

    outputs = [
        Output(display_name="输出消息", name="output_message", method="pass_message"),
    ]

    def pass_message(self) -> Message:
        self.status = self.input_message
        return self.input_message
