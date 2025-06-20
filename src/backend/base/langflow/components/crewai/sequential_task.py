from langflow.base.agents.crewai.tasks import SequentialTask
from langflow.custom.custom_component.component import Component
from langflow.io import BoolInput, HandleInput, MultilineInput, Output


class SequentialTaskComponent(Component):
    display_name: str = "Sequential Task"
    display_name_zh: str = "顺序任务"
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
        HandleInput(
            name="agent",
            display_name="代理",
            input_types=["Agent"],
            info="CrewAI 代理 that will perform the task",
            required=True,
        ),
        HandleInput(
            name="task",
            display_name="任务",
            input_types=["SequentialTask"],
            info="CrewAI 任务 that will perform the task",
        ),
        BoolInput(
            name="async_execution",
            display_name="Async Execution",
            value=True,
            advanced=True,
            info="Boolean flag indicating asynchronous task execution.",
        ),
    ]

    outputs = [
        Output(display_name="任务", name="task_output", method="build_task"),
    ]

    def build_task(self) -> list[SequentialTask]:
        tasks: list[SequentialTask] = []
        task = SequentialTask(
            description=self.task_description,
            expected_output=self.expected_output,
            tools=self.agent.tools,
            async_execution=False,
            agent=self.agent,
        )
        tasks.append(task)
        self.status = task
        if self.task:
            if isinstance(self.task, list) and all(isinstance(task, SequentialTask) for task in self.task):
                tasks = self.task + tasks
            elif isinstance(self.task, SequentialTask):
                tasks = [self.task, *tasks]
        return tasks
