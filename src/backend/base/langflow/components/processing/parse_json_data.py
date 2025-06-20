import json
from json import JSONDecodeError

import jq
from json_repair import repair_json
from loguru import logger

from langflow.custom.custom_component.component import Component
from langflow.inputs.inputs import HandleInput, MessageTextInput
from langflow.io import Output
from langflow.schema.data import Data
from langflow.schema.message import Message


class ParseJSONDataComponent(Component):
    display_name = "Parse JSON"
    display_name_zh = "JSON → 数据"
    description = "Convert and extract JSON fields."
    description_zh = "将JSON字符串转换为数据对象。"
    icon = "braces"
    name = "ParseJSONData"
    legacy: bool = True

    inputs = [
        HandleInput(
            name="input_value",
            display_name="输入",
            info="要过滤的数据对象。",
            required=True,
            input_types=["Message", "Data"],
        ),
        MessageTextInput(
            name="query",
            display_name="JQ查询",
            info="JQ查询，用于过滤数据。输入始终是JSON列表。",
            required=True,
        ),
    ]

    outputs = [
        Output(display_name="过滤后的数据", name="filtered_data", method="filter_data"),
    ]

    def _parse_data(self, input_value) -> str:
        if isinstance(input_value, Message) and isinstance(input_value.text, str):
            return input_value.text
        if isinstance(input_value, Data):
            return json.dumps(input_value.data)
        return str(input_value)

    def filter_data(self) -> list[Data]:
        to_filter = self.input_value
        if not to_filter:
            return []
        # Check if input is a list
        if isinstance(to_filter, list):
            to_filter = [self._parse_data(f) for f in to_filter]
        else:
            to_filter = self._parse_data(to_filter)

        # If input is not a list, don't wrap it in a list
        if not isinstance(to_filter, list):
            to_filter = repair_json(to_filter)
            try:
                to_filter_as_dict = json.loads(to_filter)
            except JSONDecodeError:
                try:
                    to_filter_as_dict = json.loads(repair_json(to_filter))
                except JSONDecodeError as e:
                    msg = f"Invalid JSON: {e}"
                    raise ValueError(msg) from e
        else:
            to_filter = [repair_json(f) for f in to_filter]
            to_filter_as_dict = []
            for f in to_filter:
                try:
                    to_filter_as_dict.append(json.loads(f))
                except JSONDecodeError:
                    try:
                        to_filter_as_dict.append(json.loads(repair_json(f)))
                    except JSONDecodeError as e:
                        msg = f"Invalid JSON: {e}"
                        raise ValueError(msg) from e
            to_filter = to_filter_as_dict

        full_filter_str = json.dumps(to_filter_as_dict)

        logger.info("to_filter: ", to_filter)

        results = jq.compile(self.query).input_text(full_filter_str).all()
        logger.info("results: ", results)
        return [Data(data=value) if isinstance(value, dict) else Data(text=str(value)) for value in results]
