# from langflow.field_typing import Data
from langflow.custom.custom_component.component import Component
from langflow.io import MessageTextInput, Output
from langflow.schema.data import Data


class CustomComponent(Component):
    display_name = "Custom Component"
    display_name_zh = "自定义组件"
    description = "Use as a template to create your own component."
    description_zh = "作为创建自定义组件的模板使用。"
    documentation: str = "https://docs.langflow.org/components-custom-components"
    icon = "code"
    name = "CustomComponent"

    inputs = [
        MessageTextInput(
            name="input_value",
            display_name="输入值",
            info="这是一个自定义组件的输入",
            value="Hello, World!",
            tool_mode=True,
        ),
    ]

    outputs = [
        Output(display_name="输出", name="output", method="build_output"),
    ]

    def build_output(self) -> Data:
        data = Data(value=self.input_value)
        self.status = data
        return data
