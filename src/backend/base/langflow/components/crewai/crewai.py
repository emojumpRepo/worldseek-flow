from crewai import Agent

from langflow.base.agents.crewai.crew import convert_llm, convert_tools
from langflow.custom.custom_component.component import Component
from langflow.io import BoolInput, DictInput, HandleInput, MultilineInput, Output


class CrewAIAgentComponent(Component):
    """Component for creating a CrewAI agent.

    This component allows you to create a CrewAI agent with the specified role, goal, backstory, tools,
    and language model.

    Args:
        Component (Component): Base class for all components.

    Returns:
        Agent: CrewAI agent.
    """

    display_name = "CrewAI Agent"
    display_name_zh = "CrewAI 代理"
    description = "Represents an agent of CrewAI."
    description_zh = "表示一个CrewAI代理。"
    documentation: str = "https://docs.crewai.com/how-to/LLM-Connections/"
    icon = "CrewAI"

    inputs = [
        MultilineInput(name="role", display_name="角色", info="The role of the agent."),
        MultilineInput(name="goal", display_name="Goal", info="The objective of the agent."),
        MultilineInput(name="backstory", display_name="Backstory", info="The backstory of the agent."),
        HandleInput(
            name="tools",
            display_name="工具",
            input_types=["Tool"],
            is_list=True,
            info="工具 at agents disposal",
            value=[],
        ),
        HandleInput(
            name="llm",
            display_name="Language Model",
            info="语言 model that will run the agent.",
            input_types=["LanguageModel"],
        ),
        BoolInput(
            name="memory",
            display_name="记忆",
            info="Whether the agent should have memory or not",
            advanced=True,
            value=True,
        ),
        BoolInput(
            name="verbose",
            display_name="Verbose",
            advanced=True,
            value=False,
        ),
        BoolInput(
            name="allow_delegation",
            display_name="Allow Delegation",
            info="Whether the agent is allowed to delegate tasks to other agents.",
            value=True,
        ),
        BoolInput(
            name="allow_code_execution",
            display_name="Allow Code Execution",
            info="Whether the agent is allowed to execute code.",
            value=False,
            advanced=True,
        ),
        DictInput(
            name="kwargs",
            display_name="kwargs",
            info="kwargs of agent.",
            is_list=True,
            advanced=True,
        ),
    ]

    outputs = [
        Output(display_name="代理", name="output", method="build_output"),
    ]

    def build_output(self) -> Agent:
        kwargs = self.kwargs or {}

        # Define the Agent
        agent = Agent(
            role=self.role,
            goal=self.goal,
            backstory=self.backstory,
            llm=convert_llm(self.llm),
            verbose=self.verbose,
            memory=self.memory,
            tools=convert_tools(self.tools),
            allow_delegation=self.allow_delegation,
            allow_code_execution=self.allow_code_execution,
            **kwargs,
        )

        self.status = repr(agent)

        return agent
