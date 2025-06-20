from pydantic import BaseModel, Field, create_model
from trustcall import create_extractor

from langflow.base.models.chat_result import get_chat_result
from langflow.custom.custom_component.component import Component
from langflow.helpers.base_model import build_model_from_schema
from langflow.io import (
    HandleInput,
    MessageTextInput,
    MultilineInput,
    Output,
    TableInput,
)
from langflow.schema.data import Data
from langflow.schema.table import EditMode


class StructuredOutputComponent(Component):
    display_name = "Structured Output"
    display_name_zh = "结构化输出"
    description = "Uses an LLM to generate structured data. Ideal for extraction and consistency."
    description_zh = "使用LLM生成结构化数据。适用于提取和一致性。"
    name = "StructuredOutput"
    icon = "braces"

    inputs = [
        HandleInput(
            name="llm",
            display_name="语言模型",
            info="要使用生成结构化输出的语言模型。",
            input_types=["LanguageModel"],
            required=True,
        ),
        MessageTextInput(
            name="input_value",
            display_name="输入消息",
            info="要输入到语言模型的消息。",
            tool_mode=True,
            required=True,
        ),
        MultilineInput(
            name="system_prompt",
            display_name="格式指令",
            info="要格式化输出的语言模型的指令。",
            value=(
                "You are an AI system designed to extract structured information from unstructured text."
                "Given the input_text, return a JSON object with predefined keys based on the expected structure."
                "Extract values accurately and format them according to the specified type "
                "(e.g., string, integer, float, date)."
                "If a value is missing or cannot be determined, return a default "
                "(e.g., null, 0, or 'N/A')."
                "If multiple instances of the expected structure exist within the input_text, "
                "stream each as a separate JSON object."
            ),
            required=True,
            advanced=True,
        ),
        MessageTextInput(
            name="schema_name",
            display_name="模式名称",
            info="提供输出数据模式的名称。",
            advanced=True,
        ),
        TableInput(
            name="output_schema",
            display_name="输出模式",
            info="定义模型输出的结构和数据类型。",
            required=True,
            # TODO: remove deault value
            table_schema=[
                {
                    "name": "name",
                    "display_name": "名称",
                    "type": "str",
                    "description": "指定输出字段的名称。",
                    "default": "field",
                    "edit_mode": EditMode.INLINE,
                },
                {
                    "name": "description",
                    "display_name": "描述",
                    "type": "str",
                    "description": "描述输出字段的用途。",
                    "default": "description of field",
                    "edit_mode": EditMode.POPOVER,
                },
                {
                    "name": "type",
                    "display_name": "类型",
                    "type": "str",
                    "edit_mode": EditMode.INLINE,
                    "description": ("指示输出字段的类型（例如，str、int、float、bool、dict）。"),
                    "options": ["str", "int", "float", "bool", "dict"],
                    "default": "str",
                },
                {
                    "name": "multiple",
                    "display_name": "作为列表",
                    "type": "boolean",
                    "description": "如果此输出字段应为指定类型的列表，则设置为True。",
                    "default": "False",
                    "edit_mode": EditMode.INLINE,
                },
            ],
            value=[
                {
                    "name": "field",
                    "description": "字段描述",
                    "type": "str",
                    "multiple": "False",
                }
            ],
        ),
    ]

    outputs = [
        Output(
            name="structured_output",
            display_name="结构化输出",
            method="build_structured_output",
        ),
    ]

    def build_structured_output_base(self) -> Data:
        schema_name = self.schema_name or "OutputModel"

        if not hasattr(self.llm, "with_structured_output"):
            msg = "Language model does not support structured output."
            raise TypeError(msg)
        if not self.output_schema:
            msg = "Output schema cannot be empty"
            raise ValueError(msg)

        output_model_ = build_model_from_schema(self.output_schema)

        output_model = create_model(
            schema_name,
            __doc__=f"A list of {schema_name}.",
            objects=(list[output_model_], Field(description=f"A list of {schema_name}.")),  # type: ignore[valid-type]
        )

        try:
            llm_with_structured_output = create_extractor(self.llm, tools=[output_model])
        except NotImplementedError as exc:
            msg = f"{self.llm.__class__.__name__} does not support structured output."
            raise TypeError(msg) from exc
        config_dict = {
            "run_name": self.display_name,
            "project_name": self.get_project_name(),
            "callbacks": self.get_langchain_callbacks(),
        }
        result = get_chat_result(
            runnable=llm_with_structured_output,
            system_message=self.system_prompt,
            input_value=self.input_value,
            config=config_dict,
        )
        if isinstance(result, BaseModel):
            result = result.model_dump()
        if responses := result.get("responses"):
            result = responses[0].model_dump()
        if result and "objects" in result:
            return result["objects"]

        return result

    def build_structured_output(self) -> Data:
        output = self.build_structured_output_base()

        return Data(text_key="results", data={"results": output})
