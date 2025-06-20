from langchain_text_splitters import CharacterTextSplitter

from langflow.custom.custom_component.component import Component
from langflow.io import DropdownInput, HandleInput, IntInput, MessageTextInput, Output
from langflow.schema.data import Data
from langflow.schema.dataframe import DataFrame
from langflow.utils.util import unescape_string


class SplitTextComponent(Component):
    display_name: str = "Split Text"
    display_name_zh: str = "拆分文本"
    description: str = "Split text into chunks based on specified criteria."
    description_zh: str = "根据指定条件拆分文本。"
    icon = "scissors-line-dashed"
    name = "SplitText"

    inputs = [
        HandleInput(
            name="data_inputs",
            display_name="数据或DataFrame",
            info="要拆分的文本数据。",
            input_types=["Data", "DataFrame"],
            required=True,
        ),
        IntInput(
            name="chunk_overlap",
            display_name="块重叠",
            info="块之间的重叠字符数。",
            value=200,
        ),
        IntInput(
            name="chunk_size",
            display_name="块大小",
            info=(
                "每个块的最大长度。文本首先按分隔符拆分，"
                "然后合并到此大小。"
                "大于此大小的单独拆分不会进一步拆分。"
            ),
            value=1000,
        ),
        MessageTextInput(
            name="separator",
            display_name="分隔符",
            info=(
                "要拆分的字符。使用\\n换行。"
                "示例：\\n\\n用于段落，\\n用于行，.用于句子"
            ),
            value="\n",
        ),
        MessageTextInput(
            name="text_key",
            display_name="文本键",
            info="要用于文本列的键。",
            value="text",
            advanced=True,
        ),
        DropdownInput(
            name="keep_separator",
            display_name="保留分隔符",
            info="是否保留输出块中的分隔符，以及放置位置。",
            options=["False", "True", "Start", "End"],
            value="False",
            advanced=True,
        ),
    ]

    outputs = [
        Output(display_name="块", name="dataframe", method="split_text"),
    ]

    def _docs_to_data(self, docs) -> list[Data]:
        return [Data(text=doc.page_content, data=doc.metadata) for doc in docs]

    def _fix_separator(self, separator: str) -> str:
        """Fix common separator issues and convert to proper format."""
        if separator == "/n":
            return "\n"
        if separator == "/t":
            return "\t"
        return separator

    def split_text_base(self):
        separator = self._fix_separator(self.separator)
        separator = unescape_string(separator)

        if isinstance(self.data_inputs, DataFrame):
            if not len(self.data_inputs):
                msg = "DataFrame is empty"
                raise TypeError(msg)

            self.data_inputs.text_key = self.text_key
            try:
                documents = self.data_inputs.to_lc_documents()
            except Exception as e:
                msg = f"Error converting DataFrame to documents: {e}"
                raise TypeError(msg) from e
        else:
            if not self.data_inputs:
                msg = "No data inputs provided"
                raise TypeError(msg)

            documents = []
            if isinstance(self.data_inputs, Data):
                self.data_inputs.text_key = self.text_key
                documents = [self.data_inputs.to_lc_document()]
            else:
                try:
                    documents = [input_.to_lc_document() for input_ in self.data_inputs if isinstance(input_, Data)]
                    if not documents:
                        msg = f"No valid Data inputs found in {type(self.data_inputs)}"
                        raise TypeError(msg)
                except AttributeError as e:
                    msg = f"Invalid input type in collection: {e}"
                    raise TypeError(msg) from e
        try:
            # Convert string 'False'/'True' to boolean
            keep_sep = self.keep_separator
            if isinstance(keep_sep, str):
                if keep_sep.lower() == "false":
                    keep_sep = False
                elif keep_sep.lower() == "true":
                    keep_sep = True
                # 'start' and 'end' are kept as strings

            splitter = CharacterTextSplitter(
                chunk_overlap=self.chunk_overlap,
                chunk_size=self.chunk_size,
                separator=separator,
                keep_separator=keep_sep,
            )
            return splitter.split_documents(documents)
        except Exception as e:
            msg = f"Error splitting text: {e}"
            raise TypeError(msg) from e

    def split_text(self) -> DataFrame:
        return DataFrame(self._docs_to_data(self.split_text_base()))
