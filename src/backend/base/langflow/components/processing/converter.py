from typing import Any

from langflow.custom import Component
from langflow.io import HandleInput, Output, TabInput
from langflow.schema import Data, DataFrame, Message


def convert_to_message(v) -> Message:
    """Convert input to Message type.

    Args:
        v: Input to convert (Message, Data, DataFrame, or dict)

    Returns:
        Message: Converted Message object
    """
    return v if isinstance(v, Message) else v.to_message()


def convert_to_data(v: DataFrame | Data | Message | dict) -> Data:
    """Convert input to Data type.

    Args:
        v: Input to convert (Message, Data, DataFrame, or dict)

    Returns:
        Data: Converted Data object
    """
    if isinstance(v, dict):
        return Data(v)
    return v if isinstance(v, Data) else v.to_data()


def convert_to_dataframe(v: DataFrame | Data | Message | dict) -> DataFrame:
    """Convert input to DataFrame type.

    Args:
        v: Input to convert (Message, Data, DataFrame, or dict)

    Returns:
        DataFrame: Converted DataFrame object
    """
    if isinstance(v, dict):
        return DataFrame([v])
    return v if isinstance(v, DataFrame) else v.to_dataframe()


class TypeConverterComponent(Component):
    display_name = "Type Convert"
    display_name_zh = "类型转换"
    description = "Convert between different types (Message, Data, DataFrame)"
    description_zh = "将不同类型（Message、Data、DataFrame）之间进行转换。"
    icon = "repeat"

    inputs = [
        HandleInput(
            name="input_data",
            display_name="输入",
            input_types=["Message", "Data", "DataFrame"],
            info="接受Message、Data或DataFrame三种类型作为输入",
            required=True,
        ),
        TabInput(
            name="output_type",
            display_name="输出类型",
            options=["Message", "Data", "DataFrame"],
            info="选择所需的输出数据类型",
            real_time_refresh=True,
            value="Message",
        ),
    ]

    outputs = [
        Output(
            display_name="Message输出",
            name="message_output",
            method="convert_to_message",
        )
    ]

    def update_outputs(self, frontend_node: dict, field_name: str, field_value: Any) -> dict:
        """Dynamically show only the relevant output based on the selected output type."""
        if field_name == "output_type":
            # Start with empty outputs
            frontend_node["outputs"] = []

            # Add only the selected output type
            if field_value == "Message":
                frontend_node["outputs"].append(
                    Output(
                        display_name="Message Output",
                        name="message_output",
                        method="convert_to_message",
                    ).to_dict()
                )
            elif field_value == "Data":
                frontend_node["outputs"].append(
                    Output(
                        display_name="Data Output",
                        name="data_output",
                        method="convert_to_data",
                    ).to_dict()
                )
            elif field_value == "DataFrame":
                frontend_node["outputs"].append(
                    Output(
                        display_name="DataFrame Output",
                        name="dataframe_output",
                        method="convert_to_dataframe",
                    ).to_dict()
                )

        return frontend_node

    def convert_to_message(self) -> Message:
        """Convert input to Message type."""
        input_value = self.input_data[0] if isinstance(self.input_data, list) else self.input_data

        # Handle string input by converting to Message first
        if isinstance(input_value, str):
            input_value = Message(text=input_value)

        return convert_to_message(input_value)

    def convert_to_data(self) -> Data:
        """Convert input to Data type."""
        input_value = self.input_data[0] if isinstance(self.input_data, list) else self.input_data

        # Handle string input by converting to Message first
        if isinstance(input_value, str):
            input_value = Message(text=input_value)

        return convert_to_data(input_value)

    def convert_to_dataframe(self) -> DataFrame:
        """Convert input to DataFrame type."""
        input_value = self.input_data[0] if isinstance(self.input_data, list) else self.input_data

        # Handle string input by converting to Message first
        if isinstance(input_value, str):
            input_value = Message(text=input_value)

        return convert_to_dataframe(input_value)
