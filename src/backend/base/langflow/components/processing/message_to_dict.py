from langflow.custom import Component
from langflow.io import MessageTextInput, Output, MultilineInput
from langflow.schema import Data  # 导入 Data
from typing import Dict, Optional, List


class StringToDictComponent(Component):
    """
    Converts a string of 'key: value' pairs (optionally comma-separated)
    into a Python dictionary.
    """
    display_name: str = "Message to Dictionary"
    display_name_zh: str = "Message转字典"
    description: str = "Converts a string of 'key: value' pairs (optionally comma-separated) into a Python dictionary."
    description_zh: str = "将Message对象转换为字典对象"
    icon = "code"
    name = "MessageToDictComponent"

    inputs = [
        MessageTextInput(
            name="headers_params",  # 修改为 headers_params
            display_name="Message对象",
            placeholder="传入的Message对象",
            info="要转换为字典对象的Message对象",
            value="",  # 将默认值设置为空字符串
            tool_mode=True,
        ),
        # 添加 separator 参数
        MessageTextInput(
            name="separator",
            display_name="分隔符",
            placeholder="Message对象分隔符，例如：,",
            info="使用分隔符分割Message对象，例如：Authorization: Bearer ..., Key: Value",
            value=",",
            tool_mode=True,
        ),
        MessageTextInput(
            name="keyValueSeparator",
            display_name="键值分隔符",
            placeholder="键值分隔符，例如：:",
            info="键和值之间的分隔符，例如：Authorization: Bearer ...",
            value=":",
            tool_mode=True,
        ),
        MultilineInput(  # 新增 is_json 参数
            name="is_json",
            display_name="是否为JSON",
            info="指示输入字符串是否为JSON格式",
            value="False",
        ),
    ]

    outputs = [
        Output(display_name="输出", name="output", method="build_output"),
    ]

    def build_output(self) -> Data:
        """
        Converts the input string to a dictionary.

        Returns:
            Dict:  A  dictionary.
        """
    
        output_dict: Dict = {}  # 明确指定类型
        headers_params = self.headers_params
        separator = self.separator
        keyValueSeparator = self.keyValueSeparator
        is_json_bool: bool = self.is_json.lower() == "true"  # 将 is_json 转换为布尔值
        output_list = []

        self.log(f"Input String: {self.headers_params}")
        self.log(f"Separator: {self.separator}")  # 使用 self.separator
        self.log(f"Key-Value Separator: {self.keyValueSeparator}")  # 使用 self.keyValueSeparator
        self.log(f"Is JSON: {self.is_json}")  # 使用 self.is_json

        if not self.headers_params:  # 检查输入字符串是否为空
            self.log("Input string is empty.")
            return {}  # 返回 {}

        try:
            if is_json_bool:
                output_list = [json.loads(self.headers_params)]  #  JSON 字符串放入列表
            else:
                if separator:
                    pairs = self.headers_params.split(separator)
                    self.log(f"Pairs: {pairs}")
                    for pair in pairs:
                        if keyValueSeparator in pair:
                            key, value = pair.split(keyValueSeparator, 1)
                            key = key.strip().replace('"', '')  # 移除 key 周围的引号
                            value = value.strip().replace('"', '')  # 移除 value 周围的引号
                            output_list.append({"key": key, "value": value})  # 修改输出格式, 追加到list
                            self.log(f"Added: {key} : {value}")
                        elif pair.strip():
                            self.log(
                                f"Skipping invalid key-value pair: '{pair.strip()}'"
                            )

                elif keyValueSeparator in self.headers_params:
                    key, value = self.headers_params.split(keyValueSeparator, 1)
                    key = key.strip().replace('"', '')  # 移除 key 周围的引号
                    value = value.strip().replace('"', '')  # 移除 value 周围的引号
                    output_list.append({"key": key, "value": value})  # 修改输出格式, 追加到list
                    self.log(f"Added: {key} : {value}")
                elif self.headers_params.strip():  # 增加此判断
                    self.log(
                        f"Input string does not contain the key-value separator: '{self.headers_params.strip()}'"
                    )
        except json.JSONDecodeError as e:
            self.log(f"Error decoding JSON: {e}")
            return {"error": f"Invalid JSON: {e}"}  # 返回错误信息
        except Exception as e:
            self.log(f"Error converting string to dictionary: {e}")
            return {"error": str(e)}  # 返回错误信息

        self.log(f"Output Dictionary: {output_list}")
        return output_list  #  返回字典列表
