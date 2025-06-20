from langchain_core.output_parsers import CommaSeparatedListOutputParser

from langflow.custom.custom_component.component import Component
from langflow.field_typing.constants import OutputParser
from langflow.io import DropdownInput, Output
from langflow.schema.message import Message


class OutputParserComponent(Component):
    display_name = "Output Parser"
    display_name_zh = "输出解析器"
    description = "Transforms the output of an LLM into a specified format."
    description_zh = "将LLM的输出转换为指定的格式。"
    icon = "type"
    name = "OutputParser"
    legacy = True

    inputs = [
        DropdownInput(
            name="parser_type",
            display_name="解析器",
            options=["CSV"],
            value="CSV",
        ),
    ]

    outputs = [
        Output(
            display_name="格式化指令",
            name="format_instructions",
            info="传递给提示模板以包含LLM响应的格式化指令。",
            method="format_instructions",
        ),
        Output(display_name="输出解析器", name="output_parser", method="build_parser"),
    ]

    def build_parser(self) -> OutputParser:
        if self.parser_type == "CSV":
            return CommaSeparatedListOutputParser()
        msg = "Unsupported or missing parser"
        raise ValueError(msg)

    def format_instructions(self) -> Message:
        if self.parser_type == "CSV":
            return Message(text=CommaSeparatedListOutputParser().get_format_instructions())
        msg = "Unsupported or missing parser"
        raise ValueError(msg)
