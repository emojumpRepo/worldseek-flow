from langflow.base.prompts.api_utils import process_prompt_template
from langflow.custom.custom_component.component import Component
from langflow.inputs.inputs import DefaultPromptField
from langflow.io import MessageTextInput, Output, PromptInput
from langflow.schema.message import Message
from langflow.template.utils import update_template_values


class PromptComponent(Component):
    display_name: str = "Prompt"
    display_name_zh: str = "提示词"
    description: str = "Create a prompt template with dynamic variables."
    description_zh: str = "创建带有动态变量的提示词模板。"
    icon = "braces"
    trace_type = "prompt"
    name = "Prompt"

    inputs = [
        PromptInput(name="template", display_name="模板"),
        MessageTextInput(
            name="tool_placeholder",
            display_name="工具模式占位符",
            tool_mode=True,
            advanced=True,
            info="工具模式的占位符输入。",
        ),
    ]

    outputs = [
        Output(display_name="提示词", name="prompt", method="build_prompt"),
    ]

    async def build_prompt(self) -> Message:
        prompt = Message.from_template(**self._attributes)
        self.status = prompt.text
        return prompt

    def _update_template(self, frontend_node: dict):
        prompt_template = frontend_node["template"]["template"]["value"]
        custom_fields = frontend_node["custom_fields"]
        frontend_node_template = frontend_node["template"]
        _ = process_prompt_template(
            template=prompt_template,
            name="template",
            custom_fields=custom_fields,
            frontend_node_template=frontend_node_template,
        )
        return frontend_node

    async def update_frontend_node(self, new_frontend_node: dict, current_frontend_node: dict):
        """This function is called after the code validation is done."""
        frontend_node = await super().update_frontend_node(new_frontend_node, current_frontend_node)
        template = frontend_node["template"]["template"]["value"]
        # Kept it duplicated for backwards compatibility
        _ = process_prompt_template(
            template=template,
            name="template",
            custom_fields=frontend_node["custom_fields"],
            frontend_node_template=frontend_node["template"],
        )
        # Now that template is updated, we need to grab any values that were set in the current_frontend_node
        # and update the frontend_node with those values
        update_template_values(new_template=frontend_node, previous_template=current_frontend_node["template"])
        return frontend_node

    def _get_fallback_input(self, **kwargs):
        return DefaultPromptField(**kwargs)
