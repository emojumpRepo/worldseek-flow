from typing import Any

from langflow.custom.custom_component.component import Component
from langflow.io import DataInput, DropdownInput, MessageTextInput, Output
from langflow.schema.data import Data


class DataFilterComponent(Component):
    display_name = "Filter Values"
    display_name_zh = "过滤数据值"
    description = (
        "Filter a list of data items based on a specified key, filter value,"
        " and comparison operator. Check advanced options to select match comparision."
    )
    description_zh = (
        "根据指定的键、过滤值和比较运算符过滤数据列表。"
        "检查高级选项以选择匹配比较。"
    )
    icon = "filter"
    beta = True
    name = "FilterDataValues"
    legacy = True

    inputs = [
        DataInput(name="input_data", display_name="输入数据", info="要过滤的数据列表。", is_list=True),
        MessageTextInput(
            name="filter_key",
            display_name="过滤键",
            info="要过滤的键（例如，'route'）。",
            value="route",
            input_types=["Data"],
        ),
        MessageTextInput(
            name="filter_value",
            display_name="过滤值",
            info="要过滤的值（例如，'CMIP'）。",
            value="CMIP",
            input_types=["Data"],
        ),
        DropdownInput(
            name="operator",
            display_name="比较运算符",
            options=["equals", "not equals", "contains", "starts with", "ends with"],
            info="要应用的比较运算符。",
            value="equals",
            advanced=True,
        ),
    ]

    outputs = [
        Output(display_name="过滤后的数据", name="filtered_data", method="filter_data"),
    ]

    def compare_values(self, item_value: Any, filter_value: str, operator: str) -> bool:
        if operator == "equals":
            return str(item_value) == filter_value
        if operator == "not equals":
            return str(item_value) != filter_value
        if operator == "contains":
            return filter_value in str(item_value)
        if operator == "starts with":
            return str(item_value).startswith(filter_value)
        if operator == "ends with":
            return str(item_value).endswith(filter_value)
        return False

    def filter_data(self) -> list[Data]:
        # Extract inputs
        input_data: list[Data] = self.input_data
        filter_key: str = self.filter_key.text
        filter_value: str = self.filter_value.text
        operator: str = self.operator

        # Validate inputs
        if not input_data:
            self.status = "Input data is empty."
            return []

        if not filter_key or not filter_value:
            self.status = "Filter key or value is missing."
            return input_data

        # Filter the data
        filtered_data = []
        for item in input_data:
            if isinstance(item.data, dict) and filter_key in item.data:
                if self.compare_values(item.data[filter_key], filter_value, operator):
                    filtered_data.append(item)
            else:
                self.status = f"Warning: Some items don't have the key '{filter_key}' or are not dictionaries."

        self.status = filtered_data
        return filtered_data
