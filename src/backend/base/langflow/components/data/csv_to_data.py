import csv
import io
from pathlib import Path

from langflow.custom.custom_component.component import Component
from langflow.io import FileInput, MessageTextInput, MultilineInput, Output
from langflow.schema.data import Data


class CSVToDataComponent(Component):
    display_name = "Load CSV"
    display_name_zh = "加载CSV"
    description = "Load a CSV file, CSV from a file path, or a valid CSV string and convert it to a list of Data"
    description_zh = "加载CSV文件、CSV文件路径或有效的CSV字符串并转换为Data对象列表"
    icon = "file-spreadsheet"
    name = "CSVtoData"
    legacy = True

    inputs = [
        FileInput(
            name="csv_file",
            display_name="CSV文件",
            file_types=["csv"],
            info="上传CSV文件以转换为Data对象列表",
        ),
        MessageTextInput(
            name="csv_path",
            display_name="CSV文件路径",
            info="提供CSV文件的纯文本路径",
        ),
        MultilineInput(
            name="csv_string",
            display_name="CSV字符串",
            info="粘贴一个CSV字符串直接转换为Data对象列表",
        ),
        MessageTextInput(
            name="text_key",
            display_name="文本键",
            info="要用于文本列的键。默认为'text'。",
            value="text",
        ),
    ]

    outputs = [
        Output(name="data_list", display_name="Data列表", method="load_csv_to_data"),
    ]

    def load_csv_to_data(self) -> list[Data]:
        if sum(bool(field) for field in [self.csv_file, self.csv_path, self.csv_string]) != 1:
            msg = "Please provide exactly one of: CSV file, file path, or CSV string."
            raise ValueError(msg)

        csv_data = None
        try:
            if self.csv_file:
                resolved_path = self.resolve_path(self.csv_file)
                file_path = Path(resolved_path)
                if file_path.suffix.lower() != ".csv":
                    self.status = "The provided file must be a CSV file."
                else:
                    with file_path.open(newline="", encoding="utf-8") as csvfile:
                        csv_data = csvfile.read()

            elif self.csv_path:
                file_path = Path(self.csv_path)
                if file_path.suffix.lower() != ".csv":
                    self.status = "The provided file must be a CSV file."
                else:
                    with file_path.open(newline="", encoding="utf-8") as csvfile:
                        csv_data = csvfile.read()

            else:
                csv_data = self.csv_string

            if csv_data:
                csv_reader = csv.DictReader(io.StringIO(csv_data))
                result = [Data(data=row, text_key=self.text_key) for row in csv_reader]

                if not result:
                    self.status = "The CSV data is empty."
                    return []

                self.status = result
                return result

        except csv.Error as e:
            error_message = f"CSV parsing error: {e}"
            self.status = error_message
            raise ValueError(error_message) from e

        except Exception as e:
            error_message = f"An error occurred: {e}"
            self.status = error_message
            raise ValueError(error_message) from e

        # An error occurred
        raise ValueError(self.status)
