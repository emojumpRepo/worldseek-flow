from langflow.custom.custom_component.component import Component
from langflow.helpers.data import data_to_text, data_to_text_list
from langflow.io import DataInput, MultilineInput, Output, StrInput
from langflow.schema.data import Data
from langflow.schema.message import Message


class ParseDataComponent(Component):
    display_name = "Data to Message"
    display_name_zh = "数据 → 消息"
    description = "Convert Data objects into Messages using any {field_name} from input data."
    description_zh = "使用输入数据中的任何{field_name}将数据对象转换为消息。"
    icon = "message-square"
    name = "ParseData"
    legacy = True
    metadata = {
        "legacy_name": "Parse Data",
    }

    inputs = [
        DataInput(
            name="data",
            display_name="数据",
            info="要转换为文本的数据。",
            is_list=True,
            required=True,
        ),
        MultilineInput(
            name="template",
            display_name="模板",
            info="用于格式化数据的模板。"
            "它可以包含键{text}、{data}或其他Data中的任何键。",
            value="{text}",
            required=True,
        ),
        StrInput(name="sep", display_name="分隔符", advanced=True, value="\n"),
    ]

    outputs = [
        Output(
            display_name="消息",
            name="text",
            info="数据作为单个消息，每个输入数据由分隔符分隔",
            method="parse_data",
        ),
        Output(
            display_name="数据列表",
            name="data_list",
            info="数据作为新数据列表，每个数据都由模板格式化",
            method="parse_data_as_list",
        ),
    ]

    def _clean_args(self) -> tuple[list[Data], str, str]:
        data = self.data if isinstance(self.data, list) else [self.data]
        template = self.template
        sep = self.sep
        return data, template, sep

    def parse_data(self) -> Message:
        data, template, sep = self._clean_args()
        result_string = data_to_text(template, data, sep)
        self.status = result_string
        return Message(text=result_string)

    def parse_data_as_list(self) -> list[Data]:
        data, template, _ = self._clean_args()
        text_list, data_list = data_to_text_list(template, data)
        for item, text in zip(data_list, text_list, strict=True):
            item.set_text(text)
        self.status = data_list
        return data_list
