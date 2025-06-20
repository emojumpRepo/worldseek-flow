from langflow.base.agents.crewai.tasks import HierarchicalTask
from langflow.custom.custom_component.component import Component
from langflow.io import HandleInput, MultilineInput, Output


class HierarchicalTaskComponent(Component):
    display_name: str = "Hierarchical Task"
    display_name_zh: str = "分层任务"
    description: str = "Each task must have a description, an expected output and an agent responsible for execution."
    description_zh: str = "每个任务必须有一个描述、一个期望输出和一个负责执行的代理。"
    icon = "CrewAI"
    inputs = [
        MultilineInput(
            name="task_description",
            display_name="描述",
            info="Descriptive text detailing task's purpose and execution.",
        ),
        MultilineInput(
            name="expected_output",
            display_name="Expected Output",
            info="Clear definition of expected task outcome.",
        ),
        HandleInput(
            name="tools",
            display_name="工具",
            input_types=["Tool"],
            is_list=True,
            info="List of tools/resources limited for task execution. Uses the 代理 tools by default.",
            required=False,
            advanced=True,
        ),
    ]

    outputs = [
        Output(display_name="任务", name="task_output", method="build_task"),
    ]

    def build_task(self) -> HierarchicalTask:
        task = HierarchicalTask(
            description=self.task_description,
            expected_output=self.expected_output,
            tools=self.tools or [],
        )
        self.status = task
        return task
