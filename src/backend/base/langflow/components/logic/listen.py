from langflow.custom import Component
from langflow.io import Output, StrInput
from langflow.schema.data import Data


class ListenComponent(Component):
    display_name = "Listen"
    display_name_zh = "监听"
    description = "A component to listen for a notification."
    description_zh = "一个监听通知的组件。"
    name = "Listen"
    beta: bool = True
    icon = "Radio"
    inputs = [
        StrInput(
            name="context_key",
            display_name="上下文键",
            info="要监听的上下文键",
            input_types=["Message"],
            required=True,
        )
    ]

    outputs = [Output(name="data", display_name="Data", method="listen_for_data", cache=False)]

    def listen_for_data(self) -> Data:
        """Retrieves a Data object from the component context using the provided context key.

        If the specified context key does not exist in the context, returns an empty Data object.
        """
        return self.ctx.get(self.context_key, Data(text=""))
