from core.registry import ToolRegistry
from core.executor import ToolExecutor
from utils.logger import get_logger

class MCPServer:
    def __init__(self, permissions):
        self.registry = ToolRegistry()
        self.executor = ToolExecutor(self.registry, permissions)

    def register_tool(self, name, description, handler, input_schema):
        self.registry.register(name, description, handler, input_schema)

    def handle_request(self, request):
        """
        request = {
            "role": "analyst",
            "tool": "query_sales_data",
            "params": {...}
        }
        """
        role = request["role"]
        tool_name = request["tool"]
        params = request.get("params", {})

        

        result = self.executor.execute(tool_name, params, role)

        return {
            "tool": tool_name,
            "result": result,
            "status": "success"
        }
