import json
from langflow.custom import Component
from langflow.io import MessageTextInput, Output
from langflow.schema import Data, Message


class JSONExtractorComponent(Component):
    display_name = "JSON提取器"
    description = "智能处理ChatInput输出：如果是JSON格式则提取特定字段，否则作为普通文本输出"
    documentation = "https://docs.langflow.org/components-custom-components"
    icon = "braces"
    name = "JSONExtractor"
    minimized = True

    inputs = [
        MessageTextInput(
            name="input_value",
            display_name="聊天输入",
            info="ChatInput组件的输出",
            placeholder="用户的输入",
            value="",
            tool_mode=True,
        ),
    ]

    outputs = [
        Output(display_name="用户输入", name="user_input", method="build_user_input"),
        Output(display_name="知识库参数", name="kb_params", method="build_kb_params"),
        Output(display_name="请求头参数", name="headers_params", method="build_headers_params"),
        Output(display_name="URL", name="url_value", method="build_url_value"),
    ]
    
    
    def _extract_data(self):
        try:
            raw_input = self.input_value
            
            # 检查输入是否为空或None
            if not raw_input or raw_input.strip() == "":
                self.log("输入为空，使用默认值")
                return {
                    "user_input": "", 
                    "kb_params": {}, 
                    "headers_params": {}, 
                    "url_value": ""
                }
            
            # 去除前后空白字符
            raw_input = raw_input.strip()
            
            # 尝试解析JSON
            input_json = json.loads(raw_input)
            
            # 验证解析结果是否为字典
            if not isinstance(input_json, dict):
                self.log(f"JSON解析结果不是字典类型，作为普通文本处理")
                return {
                    "user_input": raw_input, 
                    "kb_params": {}, 
                    "headers_params": {}, 
                    "url_value": ""
                }
            
            # JSON解析成功，返回解析后的数据
            self.log("JSON解析成功")
            return input_json
            
        except json.JSONDecodeError:
            # JSON解析失败，作为普通文本处理
            self.log("输入不是有效JSON格式，作为普通文本处理")
            return {
                "user_input": raw_input, 
                "kb_params": {}, 
                "headers_params": {}, 
                "url_value": ""
            }
        except Exception as e:
            self.log(f"处理输入时发生错误: {e}")
            return {
                "user_input": raw_input if raw_input else "", 
                "kb_params": {}, 
                "headers_params": {}, 
                "url_value": ""
            }

    def build_user_input(self) -> Message:
        data = self._extract_data()
        user_input = data.get("user_input", "")
        return Message(text=user_input)
        
    def build_kb_params(self) -> Data:
        data = self._extract_data()
        kb_params = data.get("kb_params", {})
        formatted_list = [{"key": k, "value": v} for k, v in kb_params.items()]
        return formatted_list
    
    def build_headers_params(self) -> Data:
        data = self._extract_data()
        headers_params = data.get("headers_params", {})
        formatted_list = [{"key": k, "value": v} for k, v in headers_params.items()]
        return formatted_list
    
    def build_url_value(self) -> Message:
        data = self._extract_data()
        url_value = data.get("url_value", "")
        return Message(text=url_value)
    