from langflow.base.data.utils import TEXT_FILE_TYPES, parallel_load_data, parse_text_file_to_data, retrieve_file_paths
from langflow.custom.custom_component.component import Component
from langflow.io import BoolInput, IntInput, MessageTextInput, MultiselectInput
from langflow.schema.data import Data
from langflow.schema.dataframe import DataFrame
from langflow.template.field.base import Output


class DirectoryComponent(Component):
    display_name = "Directory"
    display_name_zh = "目录"
    description = "Recursively load files from a directory."
    description_zh = "递归加载目录中的文件。"
    icon = "folder"
    name = "Directory"

    inputs = [
        MessageTextInput(
            name="path",
            display_name="路径",
            info="要加载文件的目录路径。默认为当前目录（'.'）",
            value=".",
            tool_mode=True,
        ),
        MultiselectInput(
            name="types",
            display_name="文件类型",
            info="要加载的文件类型。选择一个或多个类型或留空以加载所有支持的类型。",
            options=TEXT_FILE_TYPES,
            value=[],
        ),
        IntInput(
            name="depth",
            display_name="深度",
            info="要搜索的文件深度。",
            value=0,
        ),
        IntInput(
            name="max_concurrency",
            display_name="最大并发",
            advanced=True,
            info="要加载文件的最大并发数。",
            value=2,
        ),
        BoolInput(
            name="load_hidden",
            display_name="加载隐藏文件",
            advanced=True,
            info="如果为true，则加载隐藏文件。",
        ),
        BoolInput(
            name="recursive",
            display_name="递归",
            advanced=True,
            info="如果为true，则搜索将是递归的。",
        ),
        BoolInput(
            name="silent_errors",
            display_name="静默错误",
            advanced=True,
            info="如果为true，则错误不会引发异常。",
        ),
        BoolInput(
            name="use_multithreading",
            display_name="使用多线程",
            advanced=True,
            info="如果为true，则使用多线程。",
        ),
    ]

    outputs = [
        Output(display_name="Loaded Files", name="dataframe", method="as_dataframe"),
    ]

    def load_directory(self) -> list[Data]:
        path = self.path
        types = self.types
        depth = self.depth
        max_concurrency = self.max_concurrency
        load_hidden = self.load_hidden
        recursive = self.recursive
        silent_errors = self.silent_errors
        use_multithreading = self.use_multithreading

        resolved_path = self.resolve_path(path)

        # If no types are specified, use all supported types
        if not types:
            types = TEXT_FILE_TYPES

        # Check if all specified types are valid
        invalid_types = [t for t in types if t not in TEXT_FILE_TYPES]
        if invalid_types:
            msg = f"Invalid file types specified: {invalid_types}. Valid types are: {TEXT_FILE_TYPES}"
            raise ValueError(msg)

        valid_types = types

        file_paths = retrieve_file_paths(
            resolved_path, load_hidden=load_hidden, recursive=recursive, depth=depth, types=valid_types
        )

        loaded_data = []
        if use_multithreading:
            loaded_data = parallel_load_data(file_paths, silent_errors=silent_errors, max_concurrency=max_concurrency)
        else:
            loaded_data = [parse_text_file_to_data(file_path, silent_errors=silent_errors) for file_path in file_paths]

        valid_data = [x for x in loaded_data if x is not None and isinstance(x, Data)]
        self.status = valid_data
        return valid_data

    def as_dataframe(self) -> DataFrame:
        return DataFrame(self.load_directory())
