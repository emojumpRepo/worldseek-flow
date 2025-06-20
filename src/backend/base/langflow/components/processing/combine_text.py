from langflow.custom.custom_component.component import Component
from langflow.io import MessageTextInput, Output
from langflow.schema.message import Message


class CombineTextComponent(Component):
    display_name = "Combine Text"
    display_name_zh = "合并文本"
    description = "Concatenate two text sources into a single text chunk using a specified delimiter."
    description_zh = "使用指定的分隔符将两个文本源合并为一个文本块。"
    icon = "merge"
    name = "CombineText"
    legacy: bool = True

    inputs = [
        MessageTextInput(
            name="text1",
            display_name="第一个文本",
            info="要连接的第一个文本输入。",
        ),
        MessageTextInput(
            name="text2",
            display_name="第二个文本",
            info="要连接的第二个文本输入。",
        ),
        MessageTextInput(
            name="delimiter",
            display_name="分隔符",
            info="用于分隔两个文本输入的字符串。默认为空格。",
            value=" ",
        ),
    ]

    outputs = [
        Output(display_name="合并文本", name="combined_text", method="combine_texts"),
    ]

    def combine_texts(self) -> Message:
        combined = self.delimiter.join([self.text1, self.text2])
        self.status = combined
        return Message(text=combined)
