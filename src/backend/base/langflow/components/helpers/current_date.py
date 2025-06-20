from datetime import datetime
from zoneinfo import ZoneInfo, available_timezones

from loguru import logger

from langflow.custom.custom_component.component import Component
from langflow.io import DropdownInput, Output
from langflow.schema.message import Message


class CurrentDateComponent(Component):
    display_name = "Current Date"
    display_name_zh = "当前日期"
    description = "Returns the current date and time in the selected timezone."
    description_zh = "返回所选时区的当前日期和时间。"
    icon = "clock"
    name = "CurrentDate"

    inputs = [
        DropdownInput(
            name="timezone",
            display_name="时区",
            options=list(available_timezones()),
            value="UTC",
            info="选择当前日期和时间的时区。",
            tool_mode=True,
        ),
    ]
    outputs = [
        Output(display_name="当前日期", name="current_date", method="get_current_date"),
    ]

    def get_current_date(self) -> Message:
        try:
            tz = ZoneInfo(self.timezone)
            current_date = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S %Z")
            result = f"Current date and time in {self.timezone}: {current_date}"
            self.status = result
            return Message(text=result)
        except Exception as e:  # noqa: BLE001
            logger.opt(exception=True).debug("Error getting current date")
            error_message = f"Error: {e}"
            self.status = error_message
            return Message(text=error_message)
