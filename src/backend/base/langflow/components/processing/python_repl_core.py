import importlib

from langchain_experimental.utilities import PythonREPL

from langflow.custom.custom_component.component import Component
from langflow.io import CodeInput, Output, StrInput
from langflow.schema.data import Data


class PythonREPLComponent(Component):
    display_name = "Python Interpreter"
    display_name_zh = "Python解释器"
    description = "Run Python code with optional imports. Use print() to see the output."
    description_zh = "运行Python代码，可选导入。使用print()查看输出。"
    icon = "square-terminal"

    inputs = [
        StrInput(
            name="global_imports",
            display_name="全局导入",
            info="逗号分隔的模块列表，用于全局导入，例如'math,numpy,pandas'。",
            value="math,pandas",
            required=True,
        ),
        CodeInput(
            name="python_code",
            display_name="Python代码",
            info="要执行的Python代码。只有全局导入中指定的模块才能使用。",
            value="print('Hello, World!')",
            input_types=["Message"],
            tool_mode=True,
            required=True,
        ),
    ]

    outputs = [
        Output(
            display_name="结果",
            name="results",
            type_=Data,
            method="run_python_repl",
        ),
    ]

    def get_globals(self, global_imports: str | list[str]) -> dict:
        """Create a globals dictionary with only the specified allowed imports."""
        global_dict = {}

        try:
            if isinstance(global_imports, str):
                modules = [module.strip() for module in global_imports.split(",")]
            elif isinstance(global_imports, list):
                modules = global_imports
            else:
                msg = "global_imports must be either a string or a list"
                raise TypeError(msg)

            for module in modules:
                try:
                    imported_module = importlib.import_module(module)
                    global_dict[imported_module.__name__] = imported_module
                except ImportError as e:
                    msg = f"Could not import module {module}: {e!s}"
                    raise ImportError(msg) from e

        except Exception as e:
            self.log(f"Error in global imports: {e!s}")
            raise
        else:
            self.log(f"Successfully imported modules: {list(global_dict.keys())}")
            return global_dict

    def run_python_repl(self) -> Data:
        try:
            globals_ = self.get_globals(self.global_imports)
            python_repl = PythonREPL(_globals=globals_)
            result = python_repl.run(self.python_code)
            result = result.strip() if result else ""

            self.log("Code execution completed successfully")
            return Data(data={"result": result})

        except ImportError as e:
            error_message = f"Import Error: {e!s}"
            self.log(error_message)
            return Data(data={"error": error_message})

        except SyntaxError as e:
            error_message = f"Syntax Error: {e!s}"
            self.log(error_message)
            return Data(data={"error": error_message})

        except (NameError, TypeError, ValueError) as e:
            error_message = f"Error during execution: {e!s}"
            self.log(error_message)
            return Data(data={"error": error_message})

    def build(self):
        return self.run_python_repl
