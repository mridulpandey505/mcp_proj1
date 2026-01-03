from utils.errors import ToolNotFoundError, PermissionError

class ToolExecutor:
    def __init__(self, registry, permissions):
        self.registry = registry
        self.permissions = permissions

    def execute(self, tool_name, params, role):
        if tool_name not in self.permissions.get(role, []):
            raise PermissionError(f"Role '{role}' cannot execute '{tool_name}'")

        tool = self.registry.get(tool_name)
        if not tool:
            raise ToolNotFoundError(tool_name)
        
        if params is None:
            params = {}

        return tool["handler"](**params)
