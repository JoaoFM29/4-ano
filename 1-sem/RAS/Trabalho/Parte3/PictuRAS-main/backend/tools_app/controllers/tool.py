from typing import Optional, List
from models.tool import Tool


def list_tools() -> List[Tool]:
    return Tool.objects()


def find_by_id(tool_id: str) -> Optional[Tool]:
    return Tool.objects.get(id=tool_id)


def insert_tool(tool: Tool) -> Optional[Tool]:
    tool.save()
    return tool


def update_tool(tool_id: str, tool_data: dict) -> Optional[Tool]:
    tool = Tool.objects.get(id=tool_id)
    tool.update(**tool_data)
    return Tool.objects.get(id=tool_id)


def delete_tool(tool_id: str) -> Optional[Tool]:
    tool = Tool.objects.get(id=tool_id)
    tool.delete()
    return tool
