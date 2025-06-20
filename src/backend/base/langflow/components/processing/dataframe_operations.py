from langflow.custom.custom_component.component import Component
from langflow.io import BoolInput, DataFrameInput, DropdownInput, IntInput, MessageTextInput, Output, StrInput
from langflow.schema.dataframe import DataFrame


class DataFrameOperationsComponent(Component):
    display_name = "DataFrame Operations"
    display_name_zh = "DataFrame操作"
    description = "Perform various operations on a DataFrame."
    description_zh = "对DataFrame执行各种操作。"
    icon = "table"

    # Available operations
    OPERATION_CHOICES = [
        "Add Column",
        "Drop Column",
        "Filter",
        "Head",
        "Rename Column",
        "Replace Value",
        "Select Columns",
        "Sort",
        "Tail",
    ]

    inputs = [
        DataFrameInput(
            name="df",
            display_name="DataFrame",
            info="要操作的输入DataFrame。",
        ),
        DropdownInput(
            name="operation",
            display_name="操作",
            options=OPERATION_CHOICES,
            info="选择要执行的DataFrame操作。",
            real_time_refresh=True,
        ),
        StrInput(
            name="column_name",
            display_name="列名",
            info="要使用的列名。",
            dynamic=True,
            show=False,
        ),
        MessageTextInput(
            name="filter_value",
            display_name="过滤值",
            info="要过滤的值。",
            dynamic=True,
            show=False,
        ),
        BoolInput(
            name="ascending",
            display_name="升序",
            info="是否按升序排序。",
            dynamic=True,
            show=False,
            value=True,
        ),
        StrInput(
            name="new_column_name",
            display_name="新列名",
            info="重命名或添加列时的新列名。",
            dynamic=True,
            show=False,
        ),
        MessageTextInput(
            name="new_column_value",
            display_name="新列值",
            info="要填充新列的值。",
            dynamic=True,
            show=False,
        ),
        StrInput(
            name="columns_to_select",
            display_name="选择列",
            dynamic=True,
            is_list=True,
            show=False,
        ),
        IntInput(
            name="num_rows",
            display_name="行数",
            info="要返回的行数（用于head/tail）。",
            dynamic=True,
            show=False,
            value=5,
        ),
        MessageTextInput(
            name="replace_value",
            display_name="要替换的值",
            info="列中要替换的值。",
            dynamic=True,
            show=False,
        ),
        MessageTextInput(
            name="replacement_value",
            display_name="替换成的值",
            info="要替换成的值。",
            dynamic=True,
            show=False,
        ),
    ]

    outputs = [
        Output(
            display_name="DataFrame",
            name="output",
            method="perform_operation",
            info="执行操作后的结果DataFrame。",
        )
    ]

    def update_build_config(self, build_config, field_value, field_name=None):
        # Hide all dynamic fields by default
        dynamic_fields = [
            "column_name",
            "filter_value",
            "ascending",
            "new_column_name",
            "new_column_value",
            "columns_to_select",
            "num_rows",
            "replace_value",
            "replacement_value",
        ]
        for field in dynamic_fields:
            build_config[field]["show"] = False

        # Show relevant fields based on the selected operation
        if field_name == "operation":
            if field_value == "Filter":
                build_config["column_name"]["show"] = True
                build_config["filter_value"]["show"] = True
            elif field_value == "Sort":
                build_config["column_name"]["show"] = True
                build_config["ascending"]["show"] = True
            elif field_value == "Drop Column":
                build_config["column_name"]["show"] = True
            elif field_value == "Rename Column":
                build_config["column_name"]["show"] = True
                build_config["new_column_name"]["show"] = True
            elif field_value == "Add Column":
                build_config["new_column_name"]["show"] = True
                build_config["new_column_value"]["show"] = True
            elif field_value == "Select Columns":
                build_config["columns_to_select"]["show"] = True
            elif field_value in {"Head", "Tail"}:
                build_config["num_rows"]["show"] = True
            elif field_value == "Replace Value":
                build_config["column_name"]["show"] = True
                build_config["replace_value"]["show"] = True
                build_config["replacement_value"]["show"] = True

        return build_config

    def perform_operation(self) -> DataFrame:
        dataframe_copy = self.df.copy()
        operation = self.operation

        if operation == "Filter":
            return self.filter_rows_by_value(dataframe_copy)
        if operation == "Sort":
            return self.sort_by_column(dataframe_copy)
        if operation == "Drop Column":
            return self.drop_column(dataframe_copy)
        if operation == "Rename Column":
            return self.rename_column(dataframe_copy)
        if operation == "Add Column":
            return self.add_column(dataframe_copy)
        if operation == "Select Columns":
            return self.select_columns(dataframe_copy)
        if operation == "Head":
            return self.head(dataframe_copy)
        if operation == "Tail":
            return self.tail(dataframe_copy)
        if operation == "Replace Value":
            return self.replace_values(dataframe_copy)
        msg = f"Unsupported operation: {operation}"

        raise ValueError(msg)

    # Existing methods
    def filter_rows_by_value(self, df: DataFrame) -> DataFrame:
        return DataFrame(df[df[self.column_name] == self.filter_value])

    def sort_by_column(self, df: DataFrame) -> DataFrame:
        return DataFrame(df.sort_values(by=self.column_name, ascending=self.ascending))

    def drop_column(self, df: DataFrame) -> DataFrame:
        return DataFrame(df.drop(columns=[self.column_name]))

    def rename_column(self, df: DataFrame) -> DataFrame:
        return DataFrame(df.rename(columns={self.column_name: self.new_column_name}))

    def add_column(self, df: DataFrame) -> DataFrame:
        df[self.new_column_name] = [self.new_column_value] * len(df)
        return DataFrame(df)

    def select_columns(self, df: DataFrame) -> DataFrame:
        columns = [col.strip() for col in self.columns_to_select]
        return DataFrame(df[columns])

    # New methods
    def head(self, df: DataFrame) -> DataFrame:
        return DataFrame(df.head(self.num_rows))

    def tail(self, df: DataFrame) -> DataFrame:
        return DataFrame(df.tail(self.num_rows))

    def replace_values(self, df: DataFrame) -> DataFrame:
        df[self.column_name] = df[self.column_name].replace(self.replace_value, self.replacement_value)
        return DataFrame(df)
