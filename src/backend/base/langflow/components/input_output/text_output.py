from langflow.base.io.text import TextComponent
from langflow.io import MultilineInput, Output
from langflow.schema.message import Message


class TextOutputComponent(TextComponent):
    display_name = "Text Output"
    display_name_zh = "文本输出"
    description = "Sends text output via API."
    description_zh = "通过API发送文本输出。"
    icon = "type"
    name = "TextOutput"

    inputs = [
        MultilineInput(
            name="input_value",
            display_name="输入",
            info="要作为输出传递的文本。",
        ),
    ]
    outputs = [
        Output(display_name="输出文本", name="text", method="text_response"),
    ]

    def text_response(self) -> Message:
        message = Message(
            text=self.input_value,
        )
        self.status = self.input_value
        return message
