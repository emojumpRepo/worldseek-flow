from langflow.custom.custom_component.component import Component
from langflow.io import DataInput, MessageTextInput, Output
from langflow.schema.data import Data


class FilterDataComponent(Component):
    display_name = "Filter Data"
    display_name_zh = "过滤数据"
    description = "Filters a Data object based on a list of keys."
    description_zh = "根据列表中的键过滤数据对象。"
    icon = "filter"
    beta = True
    name = "FilterData"
    legacy = True

    inputs = [
        DataInput(
            name="data",
            display_name="数据",
            info="要被过滤的数据对象。",
        ),
        MessageTextInput(
            name="filter_criteria",
            display_name="过滤条件",
            info="要过滤的键列表。",
            is_list=True,
        ),
    ]

    outputs = [
        Output(display_name="过滤后的数据", name="filtered_data", method="filter_data"),
    ]

    def filter_data(self) -> Data:
        filter_criteria: list[str] = self.filter_criteria
        data = self.data.data if isinstance(self.data, Data) else {}

        # Filter the data
        filtered = {key: value for key, value in data.items() if key in filter_criteria}

        # Create a new Data object with the filtered data
        filtered_data = Data(data=filtered)
        self.status = filtered_data
        return filtered_data
