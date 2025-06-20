from langchain_core.tools import create_retriever_tool

from langflow.custom.custom_component.custom_component import CustomComponent
from langflow.field_typing import BaseRetriever, Tool
from langflow.io import HandleInput, StrInput


class RetrieverToolComponent(CustomComponent):
    display_name = "RetrieverTool"
    description = "Tool for interacting with retriever"
    name = "RetrieverTool"
    icon = "LangChain"
    legacy = True

    inputs = [
        HandleInput(
            name="retriever",
            display_name="Retriever",
            info="Retriever to interact with",
            input_types=["Retriever"],
            required=True,
        ),
        StrInput(
            name="name",
            display_name="名称",
            info="名称 of the tool",
            required=True,
        ),
        StrInput(
            name="description",
            display_name="描述",
            info="描述 of the tool",
            required=True,
        ),
    ]

    def build(self, retriever: BaseRetriever, name: str, description: str, **kwargs) -> Tool:
        _ = kwargs
        return create_retriever_tool(
            retriever=retriever,
            name=name,
            description=description,
        )
