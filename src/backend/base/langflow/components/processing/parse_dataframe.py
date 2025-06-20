from langflow.custom.custom_component.component import Component
from langflow.io import DataFrameInput, MultilineInput, Output, StrInput
from langflow.schema.message import Message


class ParseDataFrameComponent(Component):
    display_name = "Parse DataFrame"
    display_name_zh = "DataFrame → 文本"
    description = (
        "Convert a DataFrame into plain text following a specified template. "
        "Each column in the DataFrame is treated as a possible template key, e.g. {col_name}."
    )
    description_zh = (
        "将DataFrame转换为纯文本，遵循指定的模板。"
        "DataFrame中的每一列都被视为可能的模板键，例如{col_name}。"
    )
    icon = "braces"
    name = "ParseDataFrame"
    legacy = True

    inputs = [
        DataFrameInput(name="df", display_name="DataFrame", info="要转换为文本行的DataFrame。"),
        MultilineInput(
            name="template",
            display_name="模板",
            info=(
                "用于格式化每一行的模板。"
                "使用与DataFrame中的列名匹配的占位符，例如'{col1}'、'{col2}'。"
            ),
            value="{text}",
        ),
        StrInput(
            name="sep",
            display_name="分隔符",
            advanced=True,
            value="\n",
            info="用于将所有行文本连接在一起的String，构建单个文本输出。",
        ),
    ]

    outputs = [
        Output(
            display_name="文本",
            name="text",
            info="所有行合并为一个文本，每个行由模板格式化并由`sep`分隔。",
            method="parse_data",
        ),
    ]

    def _clean_args(self):
        dataframe = self.df
        template = self.template or "{text}"
        sep = self.sep or "\n"
        return dataframe, template, sep

    def parse_data(self) -> Message:
        """Converts each row of the DataFrame into a formatted string using the template.

        then joins them with `sep`. Returns a single combined string as a Message.
        """
        dataframe, template, sep = self._clean_args()

        lines = []
        # For each row in the DataFrame, build a dict and format
        for _, row in dataframe.iterrows():
            row_dict = row.to_dict()
            text_line = template.format(**row_dict)  # e.g. template="{text}", row_dict={"text": "Hello"}
            lines.append(text_line)

        # Join all lines with the provided separator
        result_string = sep.join(lines)
        self.status = result_string  # store in self.status for UI logs
        return Message(text=result_string)
