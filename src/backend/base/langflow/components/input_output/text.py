from langflow.base.io.text import TextComponent
from langflow.io import MultilineInput, Output
from langflow.schema.message import Message


class TextInputComponent(TextComponent):
    display_name = "Text Input"
    display_name_zh = "文本输入"
    description = "Get user text inputs."
    description_zh = "获取用户文本输入。"
    icon = "type"
    name = "TextInput"

    inputs = [
        MultilineInput(
            name="input_value",
            display_name="文本",
            info="要作为输入传递的文本。",
        ),
    ]
    outputs = [
        Output(display_name="输出文本", name="text", method="text_response"),
    ]

    def text_response(self) -> Message:
        return Message(
            text=self.input_value,
        )
