from langflow.custom.custom_component.component import Component
from langflow.io import DataInput, Output, StrInput
from langflow.schema.data import Data


class ExtractDataKeyComponent(Component):
    display_name = "Extract Key"
    display_name_zh = "提取键"
    description = (
        "Extract a specific key from a Data object or a list of "
        "Data objects and return the extracted value(s) as Data object(s)."
    )
    description_zh = (
        "从数据对象或数据对象列表中提取特定键，并返回提取的值作为数据对象。"
    )
    icon = "key"
    name = "ExtractaKey"
    legacy = True

    inputs = [
        DataInput(
            name="data_input",
            display_name="数据输入",
            info="要提取键的数据对象或数据对象列表。",
        ),
        StrInput(
            name="key",
            display_name="提取键",
            info="要提取的键。",
        ),
    ]

    outputs = [
        Output(display_name="提取的数据", name="extracted_data", method="extract_key"),
    ]

    def extract_key(self) -> Data | list[Data]:
        key = self.key

        if isinstance(self.data_input, list):
            result = []
            for item in self.data_input:
                if isinstance(item, Data) and key in item.data:
                    extracted_value = item.data[key]
                    result.append(Data(data={key: extracted_value}))
            self.status = result
            return result
        if isinstance(self.data_input, Data):
            if key in self.data_input.data:
                extracted_value = self.data_input.data[key]
                result = Data(data={key: extracted_value})
                self.status = result
                return result
            self.status = f"Key '{key}' not found in Data object."
            return Data(data={"error": f"Key '{key}' not found in Data object."})
        self.status = "Invalid input. Expected Data object or list of Data objects."
        return Data(data={"error": "Invalid input. Expected Data object or list of Data objects."})
