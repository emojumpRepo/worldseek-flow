from langflow.schema.table import EditMode

TOOL_OUTPUT_NAME = "component_as_tool"
TOOL_OUTPUT_DISPLAY_NAME = "工具集"
TOOLS_METADATA_INPUT_NAME = "tools_metadata"
TOOL_TABLE_SCHEMA = [
    {
        "name": "name",
        "display_name": "Tool Name",
        "type": "str",
        "description": "Specify the name of the tool.",
        "sortable": False,
        "filterable": False,
        "edit_mode": EditMode.INLINE,
        "hidden": False,
    },
    {
        "name": "description",
        "display_name": "Tool Description",
        "type": "str",
        "description": "Describe the purpose of the tool.",
        "sortable": False,
        "filterable": False,
        "edit_mode": EditMode.POPOVER,
        "hidden": False,
    },
    {
        "name": "tags",
        "display_name": "Tool Identifiers",
        "type": "str",
        "description": ("The default identifiers for the tools and cannot be changed."),
        "disable_edit": True,
        "sortable": False,
        "filterable": False,
        "edit_mode": EditMode.INLINE,
        "hidden": True,
    },
    {
        "name": "status",
        "display_name": "Enable",
        "type": "boolean",
        "description": "Indicates whether the tool is currently active. Set to True to activate this tool.",
        "default": True,
    },
]

TOOLS_METADATA_INFO = "修改工具名称和描述以帮助代理理解何时使用每个工具。"

TOOL_UPDATE_CONSTANTS = ["tool_mode", "tool_actions", TOOLS_METADATA_INPUT_NAME, "flow_name_selected"]
